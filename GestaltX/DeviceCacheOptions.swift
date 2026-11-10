// SPDX-License-Identifier: GPL-3.0-only
// Cache offsets are resolved from the device library and matched to the plist layout.
import Foundation

enum CacheOptionChoice: Int, CaseIterable, Identifiable {
    case keep, enable, restoreOriginal
    var id: Int { rawValue }
    var title: LocalizedStringResource {
        switch self {
        case .keep: "Keep Current"
        case .enable: "Enable"
        case .restoreOriginal: "Disable (Restore Original)"
        }
    }
}

struct CachedOptionFlags: Equatable, Codable, Sendable {
    let greenTea: Bool
    let notGreenTea: Bool

    static let enabled = Self(greenTea: false, notGreenTea: true)
    static let restricted = Self(greenTea: true, notGreenTea: false)
}

// Store semantic Boolean values, not offsets or bytes from the old layout.
// GestaltFileStore validates journal ownership before exposing these records.
struct CachedOptionsOriginal: Codable, Equatable, Sendable {
    let productType: String
    let build: String
    let layoutUUID: String
    let flags: CachedOptionFlags

    init(document: GestaltDocument, using resolvedLayout: MobileGestaltCacheLayout? = nil) throws {
        flags = try DeviceCacheOptions.flags(in: document, using: resolvedLayout)
        productType = document.extra[GestaltKeys.productType] as? String ?? ""
        build = document.root["CacheVersion"] as? String ?? ""
        layoutUUID = document.root["CacheUUID"] as? String ?? ""
    }

    func flags(in document: GestaltDocument, using resolvedLayout: MobileGestaltCacheLayout? = nil) throws -> CachedOptionFlags {
        // Resolve and validate the destination independently. A system update may
        // move both fields; the saved UUID is provenance, never an offset source.
        _ = try DeviceCacheOptions.validatedData(in: document, using: resolvedLayout)
        if (document.root["CacheUUID"] as? String)?.caseInsensitiveCompare(layoutUUID) != .orderedSame {
            // Keep same-layout legacy records working without model metadata.
            // Cross-layout migration requires a matching model in addition to
            // the installation/device ownership checks in GestaltFileStore.
            guard !layoutUUID.isEmpty, !productType.isEmpty,
                  document.extra[GestaltKeys.productType] as? String == productType else {
                throw GestaltFailure("Cannot restore saved additional options across cache layouts: the device model is missing or different.")
            }
        }
        return flags
    }
}

struct CachedBooleanChange: Identifiable {
    let name: String
    let offset: Int
    let before: Bool
    let after: Bool
    var id: Int { offset }
}

enum DeviceCacheOptions {
    static let wapiKey = "hiHut/WR+B9Lx/vd0WyeNg"
    static let greenTeaKey = "iyfxmLogGVIaH7aEgqwcIA"
    static let notGreenTeaKey = "4snMZS8LJkSctKypt2m+xA"

    static func validatedData(in document: GestaltDocument, using resolvedLayout: MobileGestaltCacheLayout? = nil) throws -> Data {
        let layout = try resolvedLayout ?? MobileGestaltCacheLayout.resolve(in: document)
        guard layout.matches(document), let data = document.root["CacheData"] as? Data,
              data[layout.validityOffset(for: layout.greenTeaIndex)] == 1,
              data[layout.validityOffset(for: layout.notGreenTeaIndex)] == 1,
              [layout.greenTeaOffset, layout.notGreenTeaOffset].allSatisfy({ offset in
                  data[offset] <= 1 && data[(offset + 1)..<(offset + 8)].allSatisfy { $0 == 0 }
              }),
              [greenTeaKey, notGreenTeaKey, "green-tea", "not-green-tea"].allSatisfy({ document.extra[$0] == nil }) else {
            throw GestaltFailure("The cache layout or values do not match this preset.")
        }
        return data
    }

    static func flags(in document: GestaltDocument, using resolvedLayout: MobileGestaltCacheLayout? = nil) throws -> CachedOptionFlags {
        let layout = try resolvedLayout ?? MobileGestaltCacheLayout.resolve(in: document)
        let data = try validatedData(in: document, using: layout)
        return CachedOptionFlags(greenTea: data[layout.greenTeaOffset] == 1,
                                  notGreenTea: data[layout.notGreenTeaOffset] == 1)
    }

    static func changes(from original: GestaltDocument, to edited: GestaltDocument) -> [CachedBooleanChange] {
        guard let before = original.root["CacheData"] as? Data,
              let after = edited.root["CacheData"] as? Data,
              before != after,
              let layout = try? MobileGestaltCacheLayout.resolve(in: original),
              after.count == before.count else { return [] }
        var fields: [(String, Int)] = []
        if (try? validatedData(in: original)) != nil {
            fields += [("green-tea", layout.greenTeaOffset), ("not-green-tea", layout.notGreenTeaOffset)]
        }
        if let offset = layout.wapiOffset, (try? wapi(in: original)) != nil { fields.append(("wapi", offset)) }
        return fields.compactMap { name, offset in
            guard before[offset] != after[offset] else { return nil }
            return CachedBooleanChange(name: name, offset: offset, before: before[offset] != 0, after: after[offset] != 0)
        }
    }

    static func validateEdit(from original: GestaltDocument, to edited: GestaltDocument,
                             using resolvedLayout: MobileGestaltCacheLayout? = nil) throws {
        guard original.root["CacheData"] as? Data != edited.root["CacheData"] as? Data else { return }
        let layout = try resolvedLayout ?? MobileGestaltCacheLayout.resolve(in: original)
        guard layout.matches(original), layout.matches(edited),
              let before = original.root["CacheData"] as? Data,
              let after = edited.root["CacheData"] as? Data else {
            throw GestaltFailure("The cache layout or values do not match this preset.")
        }
        let changed = Set(before.indices.filter { before[$0] != after[$0] })
        var allowed: Set<Int> = [layout.greenTeaOffset, layout.notGreenTeaOffset]
        if let offset = layout.wapiOffset { allowed.insert(offset) }
        guard changed.isSubset(of: allowed) else {
            throw GestaltFailure("This preset changes unrelated cache bytes.")
        }
        if !changed.isDisjoint(with: [layout.greenTeaOffset, layout.notGreenTeaOffset]) {
            _ = try validatedData(in: original, using: layout)
            _ = try validatedData(in: edited, using: layout)
        }
        if let offset = layout.wapiOffset, changed.contains(offset) {
            _ = try wapi(in: original, using: layout)
            _ = try wapi(in: edited, using: layout)
        }
    }

    static func wapi(in document: GestaltDocument, using resolvedLayout: MobileGestaltCacheLayout? = nil) throws -> Bool {
        let layout = try resolvedLayout ?? MobileGestaltCacheLayout.resolve(in: document)
        guard layout.matches(document), let index = layout.wapiIndex, let offset = layout.wapiOffset,
              let data = document.root["CacheData"] as? Data,
              data[layout.validityOffset(for: index)] == 1, data[offset] <= 1,
              data[(offset + 1)..<(offset + 8)].allSatisfy({ $0 == 0 }),
              document.extra[wapiKey] == nil, document.extra["wapi"] == nil else {
            throw GestaltFailure("The cache layout or values do not match this preset.")
        }
        return data[offset] == 1
    }
}

enum WAPIChoice: Int, CaseIterable, Identifiable {
    case keep, disable, restoreOriginal
    var id: Int { rawValue }
    var title: LocalizedStringResource {
        switch self {
        case .keep: "Keep Current"
        case .disable: "Disable WAPI"
        case .restoreOriginal: "Restore Original"
        }
    }
}

struct WAPIOriginal: Codable, Equatable, Sendable {
    let layoutUUID: String
    let enabled: Bool
    init(document: GestaltDocument) throws {
        enabled = try DeviceCacheOptions.wapi(in: document)
        layoutUUID = document.root["CacheUUID"] as? String ?? ""
    }
    func value(in document: GestaltDocument) throws -> Bool {
        _ = try DeviceCacheOptions.wapi(in: document)
        guard document.root["CacheUUID"] as? String == layoutUUID else {
            throw GestaltFailure("The cache layout or values do not match this preset.")
        }
        return enabled
    }
}
