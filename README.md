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

## 注意

- `allow-lan` 与 `external-controller` 已开启，建议自行添加 `secret` 后再在局域网环境使用
