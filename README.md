# 噜噜练习

每做完一道算术，演出和音乐就再热闹一档的计算练习。浏览器直接玩，也可以装安卓版。

吉祥物「噜噜」会把你输入的数字搬到算式上，答对就庆祝。题目越往后，画面和声音越热闹，最后像过节一样。答错也不会掉气势，没有游戏结束。

## 特点

- 1–6 年级计算共 58 个技能（按学习指导要领）。加法、减法、乘法、除法、竖式中间步骤、小数、分数、百分数等
- 「我的等级」模式：从实力检测的结果开始，掌握后再解锁下一个技能
- 按年级、练习、复习、技能树
- 全部做对就是 100 分。一次做对率达到 80% 以上，可以进限时加试，分数能超过 100
- 音乐和音效全部用 Web Audio API 合成（没有音频文件）
- 支持手机竖屏和电脑。电脑可以用数字键和退格键输入
- 设置里可以调节动画强度，也可以静音
- 记录全部保存在本机（localStorage），不会发送到外部

## 本地游玩

不需要构建。把 `app/` 当静态站点即可。

```bash
python -m http.server 8000 -d app
```

浏览器打开 `http://localhost:8000/`。用了 ES Modules，直接用 `file://` 打开不会运行。

## 安卓版

`shell/` 是 Flutter 壳，把 `app/` 嵌进 WebView。练习记录存在手机本机。

```bash
cd shell
rm -rf assets/game && mkdir -p assets/game && cp -a ../app/. assets/game/
flutter build apk --release
```

安装包在 `shell/build/app/outputs/flutter-apk/app-release.apk`。

推送 `v*` 标签就会自动打包。例如：

```bash
git tag v1.0.1
git push origin v1.0.1
```

GitHub Actions 打完 APK 后，会创建同名 Release，并把安装包挂上去。也可以在 Actions 页手动跑「发版打包」。

## 测试

需要 Node.js 20 以上。

```bash
node --test tests/*.test.mjs
```

## 构成

| 路径 | 内容 |
| --- | --- |
| `app/` | 游戏本体（无依赖库的 ES Modules） |
| `shell/` | 安卓壳（Flutter WebView），发版时由 GitHub Actions 打包 |
| `docs/SPEC.md` | 规格书（日文原文） |
| `docs/curriculum.md` | 年级课程与技能树设计（日文原文） |
| `docs/dopakichi.svg` | 噜噜造型原典 |
| `tests/` | 单元测试 |
| `tools/build_fonts.sh` | 重新生成字体子集（画面文案增加时运行） |

## 许可

- 源代码：MIT License
- 角色「噜噜」（原名ドパキチ），以及「噜噜练习」（原名ドパドリル）的名称和标志：不在 MIT 范围内。非营利可以自由二次创作（见下）
- 字体（`app/fonts/`）：SIL Open Font License 1.1

详情见 [LICENSE](LICENSE)。

### 关于噜噜、噜噜练习的二次创作

非营利可以不事先联系、自由使用。

- 可以：同人图、漫画、小说、动画、视频、发到社交网络、公开这个游戏的非营利分支或改造版
- 游玩视频、直播：自由。带广告收益或打赏的平台也可以
- 需要事先许可：销售周边或作品、在付费产品、服务、广告中使用等商业利用。用作其他产品或服务的名称、吉祥物、品牌，或自称官方
- 禁止：违反公序良俗的用法，以及损害角色或本项目声誉的用法

公开时请标明非官方。若与 LICENSE 英文不一致，以英文为准。
