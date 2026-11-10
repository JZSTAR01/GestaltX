import Foundation

extension DocumentTests {
    static func verifyCacheOptionMigration(in root: URL) async throws {
        let oldLayout = MobileGestaltCacheLayout(uuid: "11111111-2222-3333-4444-555555555555",
                                                slotCount: 6, greenTeaIndex: 1, notGreenTeaIndex: 4)
        let currentLayout = MobileGestaltCacheLayout.originalProfile
        let model = "migration-test-model"
        let serialKey = "VasUgeSzVyHdB27g2XpN0g"
        func fixture(_ layout: MobileGestaltCacheLayout, _ flags: CachedOptionFlags) throws -> GestaltDocument {
            var bytes = Data(repeating: 0, count: layout.byteCount)
            bytes[0] = 73 // Unrelated data must not be copied from the old cache.
            bytes[layout.greenTeaOffset] = flags.greenTea ? 1 : 0
            bytes[layout.notGreenTeaOffset] = flags.notGreenTea ? 1 : 0
            bytes[layout.validityOffset(for: layout.greenTeaIndex)] = 1
            bytes[layout.validityOffset(for: layout.notGreenTeaIndex)] = 1
            return try GestaltDocument(data: PropertyListSerialization.data(fromPropertyList: [
                "CacheUUID": layout.uuid, "CacheVersion": "build-" + layout.uuid,
                "CacheData": bytes, "OtherRoot": ["keep": true],
                "CacheExtra": [GestaltKeys.productType: model, serialKey: "migration-device", "keep": 42]
            ], format: .binary, options: 0))
        }
        func replacing(_ document: GestaltDocument, key: String, value: Any) throws -> GestaltDocument {
            var changed = document.root
            changed[key] = value
            return try GestaltDocument(data: PropertyListSerialization.data(fromPropertyList: changed, format: .binary, options: 0))
        }
        let pairs = [CachedOptionFlags.restricted, .enabled,
                     CachedOptionFlags(greenTea: false, notGreenTea: false),
                     CachedOptionFlags(greenTea: true, notGreenTea: true)]
        for (index, flags) in pairs.enumerated() {
            let old = try fixture(oldLayout, flags)
            let saved = try CachedOptionsOriginal(document: old, using: oldLayout)
            // Round-trip the existing v1 record format, as produced before the update.
            let encoded = try PropertyListEncoder().encode(saved)
            let decoded = try PropertyListDecoder().decode(CachedOptionsOriginal.self, from: encoded)
            let changedFlags = CachedOptionFlags(greenTea: !flags.greenTea, notGreenTea: !flags.notGreenTea)
            let current = try fixture(currentLayout, changedFlags)
            var restored = current
            try restored.setCacheOptions(decoded.flags(in: current))
            try DeviceCacheOptions.validateEdit(from: current, to: restored)
            try expect(restored.matches(fixture(currentLayout, flags)), "Restore semantic values into the new layout")
            let before = current.root["CacheData"] as! Data
            let after = restored.root["CacheData"] as! Data
            try expect(before.indices.filter { before[$0] != after[$0] } ==
                       [currentLayout.greenTeaOffset, currentLayout.notGreenTeaOffset],
                       "Migration changes only the new offsets, never old offsets or validity bytes")

            let directory = root.appendingPathComponent("cache-migration-\(index)")
            let backupDirectory = directory.appendingPathComponent("backups")
            try FileManager.default.createDirectory(at: backupDirectory, withIntermediateDirectories: true)
            let device = directory.appendingPathComponent("device.plist")
            let journal = backupDirectory.appendingPathComponent("OriginalValues.plist")
            let currentBytes = try current.encoded()
            try currentBytes.write(to: device)
            let journalRoot: [String: Any] = [
                "version": 1, "deviceID": "migration-installation", "identity": [serialKey: "migration-device"],
                "values": [String: [String: Any]](), "faceTimeAudio": encoded
            ]
            try PropertyListSerialization.data(fromPropertyList: journalRoot, format: .binary, options: 0).write(to: journal)
            func store(_ id: String = "migration-installation") -> GestaltFileStore {
                GestaltFileStore(deviceURL: device, backupDirectory: backupDirectory, deviceID: id,
                                 acquire: { 1 }, release: { _ in })
            }
            let files = store()
            let loaded = try await files.loadDevice()
            try expect(loaded.originalCachedOptionFlags() == flags, "Old journal survives a system layout update")
            var toRestore = loaded.document
            try toRestore.setCacheOptions(loaded.originalCachedOptionFlags())
            let committed = try await files.commit(toRestore, expected: loaded)
            try expect(committed.document.matches(restored), "Migration uses normal verified commit")
            let records = try await files.backups()
            let preWrite = records.first { $0.reason == "Before applying" }!
            try expect(try await files.backupData(preWrite) == currentBytes, "Back up the actual new-system cache before writing")
            var enabledAgain = committed.document
            try enabledAgain.setCacheOptions(changedFlags)
            _ = try await files.commit(enabledAgain, expected: committed)
            let reopened = try await store().loadDevice()
            try expect(reopened.originalCachedOptionFlags() == flags, "Subsequent writes and reload retain earliest original values")
            try expect(reopened.cachedOptionsOriginal == decoded, "Do not overwrite original provenance with the new layout")

            // Ownership failures must still precede any device write.
            do {
                _ = try await store("another-installation").loadDevice()
                throw TestFailure(message: "Foreign installation journal must be rejected")
            } catch is GestaltFailure {}
            var foreign = reopened.document
            foreign.set("another-device", for: serialKey)
            try foreign.encoded().write(to: device)
            do {
                _ = try await store().loadDevice()
                throw TestFailure(message: "Foreign device journal must be rejected")
            } catch is GestaltFailure {}
            try expect(try Data(contentsOf: device) == foreign.encoded(), "Ownership rejection leaves file unchanged")
        }

        let old = try fixture(oldLayout, .restricted)
        let saved = try CachedOptionsOriginal(document: old, using: oldLayout)
        let current = try fixture(currentLayout, .enabled)
        for modelValue in [nil, "different-model"] as [String?] {
            var wrong = current
            wrong.set(modelValue, for: GestaltKeys.productType)
            try expectThrows("Cross-layout restore requires matching model metadata") { _ = try saved.flags(in: wrong) }
        }
        let unknown = try replacing(current, key: "CacheUUID", value: "unknown-layout")
        try expectThrows("Unknown destination layout must still be rejected") { _ = try saved.flags(in: unknown) }
        for (offset, value) in [(currentLayout.greenTeaOffset, UInt8(2)),
                                (currentLayout.greenTeaOffset + 1, 1),
                                (currentLayout.validityOffset(for: currentLayout.notGreenTeaIndex), 0)] {
            var bytes = current.root["CacheData"] as! Data
            bytes[offset] = value
            let malformed = try replacing(current, key: "CacheData", value: bytes)
            try expectThrows("Migration cannot bypass slot validation") { _ = try saved.flags(in: malformed) }
        }
        let truncated = try replacing(current, key: "CacheData", value: Data((current.root["CacheData"] as! Data).dropLast()))
        try expectThrows("Migration rejects truncated cache") { _ = try saved.flags(in: truncated) }
        for key in [DeviceCacheOptions.greenTeaKey, DeviceCacheOptions.notGreenTeaKey, "green-tea", "not-green-tea"] {
            var conflicting = current
            conflicting.set(false, for: key)
            try expectThrows("Migration rejects conflicting overrides") { _ = try saved.flags(in: conflicting) }
        }
        // Identical UUIDs differing only in letter case are not a migration.
        var noModel = current
        noModel.set(nil, for: GestaltKeys.productType)
        let sameLayout = try CachedOptionsOriginal(document: noModel)
        let lowercased = try replacing(noModel, key: "CacheUUID", value: currentLayout.uuid.lowercased())
        try expect(sameLayout.flags(in: lowercased) == .enabled, "Case-only UUID differences preserve legacy behavior")
        print("PASS: cross-layout option restore, relocated bytes, all Boolean pairs, journal persistence and migration guards.")
    }
}
