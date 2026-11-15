# Clash

个人使用的 [mihomo](https://wiki.metacubex.one/)（Clash Meta）配置文件，配合 FlClash 使用。

## 使用

- 配置文件：[yaml/clash.yaml](yaml/clash.yaml)
- 使用前将 `proxy-providers.provider1.url` 替换为自己的机场订阅链接

## 主要特性

- 分流规则：AI / YouTube / Google / GitHub / Microsoft / Apple / Telegram / Netflix 等常用服务独立策略组
- 广告拦截（adblockmihomolite 规则集）
- fake-ip 模式 + 国内外 DNS 分流（阿里 / 腾讯 DoH 直连解析国内域名）
- 已适配 Tailscale 共存：Tailscale 相关域名、网段与进程直连，`ts.net` 不被 fake-ip 劫持
- 内置 zashboard 面板（external-ui）

## 图标库

- 图标索引（可在 FlClash / Stash / Shadowrocket 等支持图标库的客户端中订阅）：
  `https://raw.githubusercontent.com/bupangde/Clash/main/icons.json`
- 格式与 [fmz200/wool_scripts 图标库](https://raw.githubusercontent.com/fmz200/wool_scripts/main/icons/icons-all.json) 一致：`{ name, description, icons: [{ name, url }] }`
- 图标文件放在 `icon/` 目录，支持 png / jpg / jpeg / webp / gif / bmp / svg

### 自动更新

往 `icon/` 目录上传（或删除、重命名）图标并推送到 `main` 后，[GitHub Actions](.github/workflows/update-icons-json.yml) 会自动重新生成 `icons.json` 并回写仓库，**无需手动维护索引**。

本地也可以手动重新生成：

```bash
python scripts/generate_icons_json.py
```

脚本默认从 `git remote origin` 解析 `OWNER/REPO`、从当前分支解析分支名；可用 `--repo` / `--branch` / `--output` 覆盖。

## 注意

- `allow-lan` 与 `external-controller` 已开启，建议自行添加 `secret` 后再在局域网环境使用
