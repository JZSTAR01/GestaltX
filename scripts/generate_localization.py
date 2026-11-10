from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = '''
Cannot restore saved additional options across cache layouts: the device model is missing or different.	无法跨缓存布局恢复已保存的附加选项：设备机型信息缺失或不一致。
WAPI	WAPI
Disable WAPI	关闭 WAPI
Restore Original	恢复原值
Special Thanks	特别鸣谢

Supported	支持
Unsupported	不支持
Welcome	欢迎
Welcome to GestaltX	欢迎使用 GestaltX
MobileGestalt Editor	MobileGestalt 编辑工具
Disclaimer	免责说明
I Understand, Continue	我已了解，继续
System access and available features vary by OS version, device and signing.	系统文件访问和功能可用性因系统版本、设备与签名而异。
Changing MobileGestalt may cause system instability, missing features or a boot loop. Recovering the device may require a restore.	修改 MobileGestalt 可能导致系统不稳定、功能异常或无法开机，严重时可能需要恢复设备。
Back up your device before making changes, and export a copy of the original plist.	修改前请备份设备，并导出一份原始 plist，请谨慎操作。
Capability flags cannot add missing hardware. Some changes require a device restart.	功能标记无法增加设备缺少的硬件，部分更改需要重新启动设备才能生效。
Use only devices you own or are authorized to manage. You are responsible for the changes you choose to apply.	仅在你拥有或获授权管理的设备上使用，并自行承担所选修改带来的风险。
This software is provided without warranty. Read the included license before use.	本软件不提供任何担保，使用前请阅读随附的开源许可证。

GitHub Repository	GitHub 仓库

Credits & Licenses	鸣谢与许可
License	许可证
Respring Technique	注销方法
Read Again	重新读取

A device restart may be required.	可能需要重新启动设备才能生效。
Restart the device after changing the region.	更改地区后需要重新启动设备。
Some changes require a device restart.	部分更改需要重新启动设备。
Restart required. Apple Intelligence also depends on device and region.	需要重新启动设备。Apple 智能还取决于机型与地区。
Restart the device, then reopen Settings. Pencil hardware support is still required.	重新启动设备后再打开“设置”，仍需要 Apple Pencil 硬件支持。
Respring first. Restart the device if the change does not appear.	先执行注销，若未生效则重新启动设备。
Write verified. Some features require a device restart.	写入已验证。部分功能需要重新启动设备才能生效。

Model	机型
Status	状态
Connected	已连接
Local File	本地文件
Not Loaded	未读取
Reading…	正在读取…
Read MobileGestalt	读取 MobileGestalt
Import Plist	导入 plist
Actions	操作
Apply Changes	应用更改
Respring Required	需要注销
Log	日志
Experimental settings. Back up before applying.	实验性设置，请在应用前备份。
No Backups	暂无备份
A backup is created before each write.	每次写入前会自动备份。
This will attempt to restart SpringBoard using NeoSpring.	将通过 NeoSpring 尝试重新启动 SpringBoard。
GitHub Projects	GitHub 项目
GNU GPL v3	GNU GPL v3

Date	日期
Enter an ISO 8601 date, such as 2026-11-09T12:00:00Z.	请输入 ISO 8601 日期，例如 2026-11-09T12:00:00Z。
Tools	工具
Backups	备份
About	关于
GestaltX	GestaltX
OK	好
Cancel	取消
Apply	应用
Done	完成
Close	关闭
More	更多
Ready	就绪
Enable	启用
Disable	停用
Disable (Restore Original)	停用（恢复原值）
Remove Added Fields	移除新增字段
Disabling restores the recorded original values. Use Remove Added Fields only for fields you know were originally absent.	停用会恢复已记录的原值。确认原本不存在的字段，才使用“移除新增字段”。
Original values could not be read. No system changes were made.	无法读取原值记录，未修改系统文件。
The original-value record belongs to a different device.	原值记录属于其他设备。
Original values could not be saved and verified. No system write was started.	无法保存并验证原值记录，未开始写入系统文件。
The selected added fields must be removed before applying.	请先移除选中的新增字段，再应用更改。
Keep Current	保持当前值
Display	显示
Device	设备
iPad	iPad
Intelligence	智能
Advanced	高级
String	字符串
Integer	整数
Real	浮点数
Boolean	布尔值
Data	数据
Array	数组
Dictionary	字典
Make your device your own.	让设备更合你意。
Capabilities	功能设置
Choose what to change.	选择你想调整的功能。
Connect or open a plist to start editing.	连接设备或打开 plist，开始编辑。
Quick Actions	快捷操作
Keep a copy. Refresh when ready.	先留一份备份，准备好后再刷新。
Back Up	备份
Export Plist	导出 plist
Respring	注销
Changes are verified. Respring when you are ready.	更改已验证，准备好后可执行注销。
Session Log	操作日志
Open Plist…	打开 plist…
Connect to Device	连接设备
Pending Changes	待应用更改
%lld fields changed	已更改 %lld 个字段
Review	查看更改
On Device	本机模式
Local Document	本地文稿
Your Device	你的设备
Not Connected	未连接
%lld fields	%lld 个字段
Live snapshot	当前快照
Open the system cache, or work with a plist from Files.	读取系统缓存，或编辑“文件”中的 plist。
Connecting…	正在连接…
Connect	连接
Open File	打开文件
Refresh	刷新
System-cache access depends on OS and signing. Upstream lists SystemGroup access for iOS 27; iOS 26 can use local files.	系统缓存的访问取决于系统版本与签名。上游仅列明 iOS 27 可访问 SystemGroup；iOS 26 可编辑本地文件。
Dynamic Island Layout	灵动岛布局
A different layout can affect the status bar and keyboard. Keep a backup.	更改布局可能影响状态栏与键盘，请保留备份。
Device Identity	设备标识
Change Model Name	更改机型名称
Model Name	机型名称
Sales Region	销售地区
Region Code	地区代码
Usually, changing the region code is enough. There is no need to change Sales Region.	通常只需修改地区代码，无需更改销售地区。
* If you previously changed Sales Region, restore your device's original sales region and apply it first.	* 之前修改过销售地区的用户，请先改回设备原本的销售地区并应用。
Changing the sales-region suffix may cause verification tools to report a mismatch with factory information.	更改销售地区后缀可能导致验机工具提示与出厂信息不匹配。
Changing a region flag does not guarantee Apple Intelligence or region-restricted services.	更改地区标记并不保证可用 Apple 智能或受地区限制的服务。
Experimental	实验性
Presets	预设
Selections are staged until you review and apply them. Capability flags do not add missing hardware.	所选更改会先暂存，查看后再统一应用。功能标记无法增加设备缺少的硬件。
iPadOS CacheData conversion is not enabled for these OS builds.	这些系统版本尚未开放 iPadOS CacheData 转换。
Unverified byte-offset patches are excluded. Use supported presets or inspect individual fields.	未接入未经验证的偏移补丁。你可以使用已有预设或查看具体字段。
Review Changes	查看更改
No Document Open	尚未打开文稿
Connect or open a plist in Tools to browse its fields.	在“工具”中连接设备或打开 plist，即可查看字段。
%lld bytes	%lld 字节
Raw system fields. Review the key and type before saving.	这里是原始系统字段，保存前请核对键名与类型。
Search keys and values	搜索键名与值
Add Field	添加字段
Delete	删除
Delete this field?	删除这个字段？
The deletion is staged. The device file changes only after you apply.	删除操作会先暂存，应用后才会修改设备文件。
Key	键名
Field Key	字段键名
Value	值
Type	类型
Use an XML plist fragment, including the array or dict tags. Nested data and numeric types are preserved.	请输入包含 array 或 dict 标签的 XML plist 片段。嵌套的数据与数字类型会被保留。
Data values use Base64 encoding.	数据值使用 Base64 编码。
Edit Field	编辑字段
Stage	暂存
Write to this device	写入本机
Save local document	保存本地文稿
A backup is created before writing. The result is read back and compared.	写入前会创建备份，写入后会回读并比较内容。
This edits the opened file in GestaltX. Export it to save a copy; the system file is not changed.	仅编辑 GestaltX 中打开的文件。请导出以保存副本，系统文件不会被修改。
Apply to Device	应用到设备
Save Local Changes	保存本地更改
Discard Changes	放弃更改
Apply these changes?	应用这些更改？
Incorrect system values can affect device behavior. A verified backup will be kept. No respring is triggered automatically.	错误的系统值可能影响设备运行。应用会保留经过验证的备份，且不会自动执行注销。
The current local document will be backed up before saving your edits.	保存更改前会先备份当前本地文稿。
Before	更改前
After	更改后
Not present	不存在
Create Backup	创建备份
Device backups stay linked to this installation. Imported files are kept separate.	本机备份与本次安装关联，导入文件的备份会单独保存。
Your Safety Net	多一份保障
Backups appear here before each write. You can also make one anytime.	每次写入前会自动备份，你也可以随时手动备份。
Device Backup	本机备份
Local File Backup	本地文件备份
Open	打开
Export	导出
Restore	恢复
Initial backup	首次备份
Original values snapshot	修改前原值快照
Revert	还原
Original values restored.	已还原原值。
Restore this backup?	恢复这个备份？
The current document is backed up first. Device restores are verified after writing.	会先备份当前文稿。本机恢复会在写入后进行验证。
Delete this backup?	删除这个备份？
This removes the local backup permanently. It does not change the device file.	本地备份将被永久删除，设备文件不会被修改。
No activity yet.	暂无操作记录。
Clear	清空
Respring now?	立即注销？
NeoSpring will attempt to restart SpringBoard. Save your work first. It may not work on every OS build.	NeoSpring 将尝试重新启动 SpringBoard，请先保存其他应用中的工作。部分系统版本可能不适用。
Dynamic Island, Always-On and Liquid Glass	灵动岛、全天候显示与液态玻璃
Charging, buttons and device identity	充电、按键与设备标识
Stage Manager and app compatibility	台前调度与应用兼容性
Region and generative model capabilities	地区与生成式模型功能
Internal features and research settings	内部功能与研究设置
Dynamic Island	灵动岛
Enable the alternate Dynamic Island capability.	启用备用灵动岛功能标记。
Always-On Display	全天候显示
Display behavior depends on the panel. May increase power use and burn-in risk.	显示效果取决于屏幕硬件，可能增加耗电与烧屏风险。
AOD Vibrancy	全天候显示色彩
Adjust Always-On rendering capabilities.	调整全天候显示的渲染功能标记。
Liquid Glass Low-Power Rendering	液态玻璃低性能渲染
Use the low-performance rendering capability on iOS 26 and later.	在 iOS 26 及以后版本启用低性能渲染标记。
Boot & Shutdown Chime	开关机提示音
Expose the startup and shutdown sound capability.	显示开关机提示音功能。
Charge Limit	充电上限
Show charging limit settings. Actual charging control depends on hardware.	显示充电上限设置，实际充电控制仍取决于硬件。
Tap to Wake	轻点唤醒
Expose tap-to-wake on devices where it is hidden.	在隐藏此功能的设备上显示轻点唤醒选项。
Camera Control	相机控制
Show Camera Control settings. Does not add a physical button.	显示相机控制设置，不会为设备增加实体按钮。
Action Button	操作按钮
Show the Action Button settings page.	显示操作按钮设置页面。
Apple Pencil	Apple Pencil
Expose Apple Pencil settings. Hardware support is still required.	显示 Apple Pencil 设置，仍需要硬件支持。
Stage Manager	台前调度
Expose Stage Manager support. Layout behavior varies by device.	显示台前调度功能，布局效果因设备而异。
iPad App Compatibility	iPad 应用兼容性
Allow iPad app compatibility types on iPhone.	允许 iPhone 使用 iPad 应用兼容类型。
Apple Intelligence Capability	Apple 智能功能标记
Set the generative models capability. Availability also depends on hardware, region and Apple services.	设置生成式模型功能标记，可用性仍取决于硬件、地区与 Apple 服务。
Apple Internal Features	Apple 内部功能
Expose internal menus. Some system services may behave differently.	显示内部菜单，部分系统服务的行为可能发生变化。
Internal Storage View	内部存储视图
Show internal storage categories. Experimental on iPad.	显示内部存储分类，在 iPad 上属于实验性功能。
Security Research Device	安全研究设备
Change the SRD capability flag. This does not turn the device into an Apple SRD.	更改 SRD 功能标记，不会将设备变成 Apple 官方安全研究设备。
United States	美国
Hong Kong	中国香港
Japan	日本
China (Mainland)	中国大陆
Taiwan	中国台湾
United Kingdom	英国
Connect to your device or open a plist.	连接设备或打开 plist。
Checking device access…	正在检查设备访问权限…
Device connected	设备已连接
Device access unavailable	无法访问设备
Local file opened	已打开本地文件
Changes verified on device	本机更改已验证
Local changes saved	本地更改已保存
Changes verified on device. Respring to refresh supported features.	本机更改已验证，可执行注销以刷新受支持的功能。
Local changes saved. Export the plist to keep a copy.	本地更改已保存，请导出 plist 以保留副本。
Backup saved	备份已保存
Backup restored and verified.	备份已恢复并通过验证。
Backup opened as a local document.	已将备份打开为本地文稿。
Manual backup	手动备份
Before editing	编辑前备份
Before applying	应用前备份
Before restoring	恢复前备份
Enter a valid whole number.	请输入有效的整数。
Enter a finite decimal number.	请输入有限的十进制数。
Use true or false for a Boolean value.	布尔值请输入 true 或 false。
Enter valid Base64 data.	请输入有效的 Base64 数据。
Enter an XML plist array or dictionary fragment.	请输入有效的 XML plist 数组或字典片段。
Choose a MobileGestalt plist with a CacheExtra dictionary.	请选择包含 CacheExtra 字典的 MobileGestalt plist。
The edited document is not a valid property list.	编辑后的文稿不是有效的属性列表。
MobileGestalt access was denied. Check the OS version and App Group signing.	MobileGestalt 访问被拒绝，请检查系统版本与 App Group 签名。
The backup could not be verified. No system write was started.	备份验证失败，未开始写入系统文件。
This backup does not belong to this device. Open it as a local file instead.	此备份不属于当前设备，请将其作为本地文件打开。
MobileGestalt changed since it was loaded. Refresh before applying your edits.	MobileGestalt 已在加载后发生变化，请刷新后再应用更改。
The write did not match the readback.	写入内容与回读结果不一致。
The original file could not be restored.	无法恢复原始文件。
Write verification and recovery failed. Keep the backup and recover the device file before trying again.	写入验证与恢复均失败。请保留备份，恢复设备文件后再尝试。
The write failed. The previous file was restored and verified.	写入失败，之前的文件已恢复并通过验证。
Device access is unavailable in the Simulator. Open a plist to explore GestaltX.	模拟器无法访问设备文件，你可以打开 plist 体验 GestaltX。
The signed app has no usable App Group. Enable its App Group capability and sign it again.	当前签名没有可用的 App Group，请启用对应能力后重新签名。
Choose a plist smaller than 16 MB.	请选择小于 16 MB 的 plist。
Enter a field key.	请输入字段键名。
Load a document first.	请先加载文稿。
That key already exists. Edit the existing field instead.	此键名已存在，请直接编辑已有字段。
Enter a model name before applying.	请先输入机型名称再应用。
A little more possibility.	多一点可能。
More Projects by huamidev	huamidev 的更多项目
Minimum OS	最低系统版本
Languages	语言
Compatibility	兼容性
Credits	鸣谢
worse_query sandbox escape	worse_query 沙盒逃逸原语
Original WebKit respring technique	原始 WebKit 注销方法
Swift implementation of the respring technique	注销方法的 Swift 实现
NeoSpring project and respring research	NeoSpring 项目与注销研究
GPL-licensed respring adaptation	采用 GPL 许可的注销适配实现
MobileGestalt key research	MobileGestalt 键名研究
MobileGestalt preset research	MobileGestalt 预设研究
MobileGestalt workflow reference	MobileGestalt 工作流参考
Open Source	开源许可
Third-Party Notices	第三方声明
GestaltX is independent software. It is not affiliated with Apple or the credited projects.	GestaltX 是独立软件，与 Apple 及鸣谢项目没有隶属关系。
worse_query	worse_query
Available paths and MobileGestalt presets vary by device and OS build.	可访问的路径及 MobileGestalt 预设因设备与系统版本而异。
Read Upstream Compatibility	查看上游兼容性说明
MobileGestalt Access	MobileGestalt 访问
iOS 27: access is checked on the device.	iOS 27：通过本机实际探测访问权限。
iOS 26: SystemGroup access is not claimed by upstream. Local plist editing is available.	iOS 26：上游未声明支持 SystemGroup 访问，可编辑本地 plist。
A correctly provisioned App Group is required. Export and backup are available for any document you can open.	需要正确配置并签名 App Group。能够打开的文稿均可导出与备份。
NeoSpring	NeoSpring
NeoSpring attempts a SpringBoard refresh using WebKit. Its effectiveness varies by OS build. Some MobileGestalt changes may still need a manual device restart.	NeoSpring 使用 WebKit 尝试刷新 SpringBoard，效果因系统版本而异。部分 MobileGestalt 更改仍可能需要手动重新启动设备。
License text could not be loaded.	无法加载许可文本。
Respring did not finish.	注销未完成。
Refreshing SpringBoard…	正在刷新 SpringBoard…
This OS build may not support the technique. You can close this screen and try a manual restart later.	当前系统版本可能不支持此方法。你可以关闭此页面，稍后手动重新启动设备。
Your device may briefly return to the Lock Screen.	设备可能会短暂返回锁定屏幕。
The cache layout or values do not match this preset.	缓存布局或数值与此预设不符。
This preset changes unrelated cache bytes.	此预设更改了无关的缓存字节。
Unable to resolve this device's MobileGestalt cache layout.	无法解析此设备的 MobileGestalt 缓存布局。
Importing Plist…	正在导入 plist…
Share one MobileGestalt plist at a time.	请每次分享一个 MobileGestalt plist 文件。
Sign GestaltX and its share extension with the same App Group, then try again.	请为 GestaltX 和分享扩展签入同一个 App Group 后重试。
The shared plist could not be read. Share it again.	无法读取分享的 plist，请重新分享。
A shared plist is waiting. Save or discard your current changes, then import it.	有分享的 plist 等待导入，请先保存或放弃当前更改。
Save or discard your current changes before opening another plist.	请先保存或放弃当前更改，再打开另一个 plist。
Import	导入
Open GestaltX to confirm importing the plist.	请打开 GestaltX 确认导入 plist。
This device's identity could not be verified. Read MobileGestalt on this device and try sharing again.	无法核验本机身份，请先读取本机 MobileGestalt 后重新分享。
This plist belongs to another device and cannot be imported.	此 plist 的设备标识与本机不符，无法导入。
This plist does not contain enough device identifiers to verify ownership.	此 plist 缺少足够的设备标识，无法确认属于本机。
Additional Options	附加选项
MG Control	MG 控制
Read MobileGestalt in Tools, or share this device's plist to GestaltX.	在工具中读取 MobileGestalt，或将本机 plist 分享到 GestaltX。
This plist has been verified for this device. Import it?	已核验此 plist 属于本机，是否导入？
This plist's device proof could not be verified on this device.	无法在本机验证此 plist 的设备凭证。
This plist uses a different system cache layout and cannot be restored.	此 plist 的系统缓存布局与本机不符，无法恢复。
Restore Imported Plist	恢复导入的 plist
The current device file will be backed up before restoring. Restart the device afterward.	恢复前会备份当前设备文件，完成后请重启设备。
Share this device's plist to GestaltX to edit its keys and values or restore a verified backup. Export a copy from GestaltX first to keep a device-bound proof.	现在可将本机 plist 分享到 GestaltX，核验后导入、增删改键值并恢复。建议先从 GestaltX 导出一份带本机校验凭证的备份。
Canada	加拿大
Model Number	型号号码
A device restart may be required after changing the model number.	修改型号号码后可能需要重启设备。
Listed values apply to iPhone 18 Pro and iPhone 18 Pro Max only. Choosing a model number that does not match your hardware can make verification tools report a mismatch.	以下号码仅适用于 iPhone 18 Pro 和 iPhone 18 Pro Max。选择与硬件不符的号码，可能导致验机工具报告不匹配。
A3472 — 18 Pro · United States	A3472 — 18 Pro · 美国
A3713 — 18 Pro · Canada / Japan	A3713 — 18 Pro · 加拿大／日本
A3714 — 18 Pro · Other regions	A3714 — 18 Pro · 其他地区
A3715 — 18 Pro · China mainland	A3715 — 18 Pro · 中国大陆
A3473 — 18 Pro Max · United States	A3473 — 18 Pro Max · 美国
A3716 — 18 Pro Max · Canada / Japan	A3716 — 18 Pro Max · 加拿大／日本
A3717 — 18 Pro Max · Other regions	A3717 — 18 Pro Max · 其他地区
A3718 — 18 Pro Max · China mainland	A3718 — 18 Pro Max · 中国大陆
The artwork field is not a dictionary. Edit it in MG Control before using these presets.	artwork 字段不是字典，请先在 MG 控制中编辑此字段，再使用这些预设。
High-Luminance Always-On Display	高亮度始终显示
Allow Always-On Display to reach a higher brightness level.	允许“始终显示”达到更高亮度。
Always-On Display Flipbook	始终显示翻页组件
Enable AOD flipbook widgets on the Lock Screen.	在锁屏上启用 AOD 翻页小组件。
AOD Flipbook Count	AOD 翻页数量
Set how many AOD flipbook entries are allowed. Experimental; the accepted range varies by build.	设置允许的 AOD 翻页条目数量。实验性功能，可用范围因系统版本而异。
Disable Wallpaper Parallax	关闭壁纸视差
Stop the wallpaper from moving with device motion.	停止壁纸随设备移动产生位移。
HDR Photo Display	HDR 照片显示
Enable true HDR rendering for photos.	为照片启用真正的 HDR 渲染。
Pulse Width Modulation	脉宽调制 (PWM)
Advertise PWM display support. Actual dimming behavior depends on the panel.	声明支持 PWM 调光。实际调光行为取决于屏幕面板。
DisplayPort Output	DisplayPort 输出
Advertise DisplayPort output support. Compatible hardware is still required.	声明支持 DisplayPort 输出，仍需要兼容硬件。
Collision SOS	车祸检测 SOS
Show collision detection in Emergency SOS settings. Hardware support is still required.	在“紧急 SOS”设置中显示车祸检测，仍需要硬件支持。
Audio Mix	音频混音
Enable the audio mix capability for supported media.	为支持的媒体启用音频混音能力。
Spatial FaceTime Audio	FaceTime 空间音频
Enable spatial audio playback for FaceTime.	为 FaceTime 启用空间音频播放。
Internal Settings Bundle	内部设置包
Expose Apple's internal settings bundle. Some system services may behave differently.	显示 Apple 内部设置包。部分系统服务可能表现异常。
On-Device Siri	端侧 Siri
Advertise on-device Siri understanding. Availability depends on hardware and region.	声明支持端侧 Siri 理解，可用性取决于硬件与地区。
Audio Intelligence	音频智能
Advertise the iOS 27 audio intelligence capability.	声明 iOS 27 音频智能能力。
Personal Translator	个人翻译
Advertise the personal translator capability.	声明个人翻译能力。
Photos Clean Up	照片 Clean Up
Advertise the photos inpainting (Clean Up) capability.	声明照片修复（Clean Up）能力。
Handwriting Synthesis	手写合成
Advertise the handwriting synthesis model capability.	声明手写合成模型能力。
Always-Listening Hey Siri	常听 Hey Siri
Advertise always-listening Hey Siri support.	声明支持常听 Hey Siri。
'''
entries = {}
for line in TRANSLATIONS.strip().splitlines():
    if not line.strip():
        continue
    key, value = line.split('\t', 1)
    entries[key] = {'localizations': {lang: {'stringUnit': {'state': 'translated', 'value': text}} for lang, text in [('en', key), ('zh-Hans', value)]}}
for translation_file in sorted((ROOT / 'localization').glob('*.json')):
    locale = translation_file.stem
    translations = json.loads(translation_file.read_text())
    missing = set(entries) - set(translations)
    if missing:
        raise ValueError(f'{locale}: missing {len(missing)} translations')
    for key in entries:
        entries[key]['localizations'][locale] = {'stringUnit': {'state': 'translated', 'value': translations[key]}}
(ROOT / 'GestaltX/Localizable.xcstrings').write_text(json.dumps({'sourceLanguage': 'en', 'strings': entries, 'version': '1.0'}, ensure_ascii=False, indent=2) + '\n')
print(f'Generated {len(entries)} strings in {len(next(iter(entries.values()))["localizations"])} locales.')
