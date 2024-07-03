# pdf signer

使用自签名证书对PDF进行签名并加上可见签章的工具，代码来自https://pengs.top/pdf-sign/

适用于Windows, Mac OS X,Linux

以下内容原文来自[Peng's Blog](https://pengs.top/pdf-sign/)

## 使用方法 - 省流版

下载本仓库代码

```
pip install pip install pyhanko[opentype]
```
```
openssl genrsa -aes128 -out myself.key 2048
```
```
openssl req -new -days 365 -key myself.key -out myself.csr
```
```
openssl x509 -in myself.csr -out myself.crt -req -signkey myself.key -days 365
```
```
openssl pkcs12 -export -out myself.pfx -inkey myself.key -in myself.crt
```
```
python stamp.py
```

写的比较简略，但应该能看懂，看不懂的看原文：

https://pengs.top/pdf-sign

文中代码即本仓库stamp.py

## 致谢

这个小工具使用了开源的`pyhanko`库。

## 效果

![图片](https://github.com/Micraow/pdf_signer/assets/48644801/93037f45-bc76-45e3-9253-1ebe68f840cf)

扫描结果：

![demo](https://img.pengs.top/i/2024/07/03/Screenshot_2024-07-03-13-38-20-614_com.xiaomi.scanner.webp)

我还整了中英双语。
