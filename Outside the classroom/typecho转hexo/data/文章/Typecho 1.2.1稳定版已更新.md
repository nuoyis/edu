---
title: Typecho 1.2.1稳定版已更新
date: 2023-06-07 14:02:30
categories: uncategorized
tags: []
---

>目前，typecho 1.2.1正式版已经提供下载通道，直通车:[https://github.com/typecho/typecho/releases/tag/v1.2.1][1].
本次官方更新了以下内容:

> Fix checkVersion by @sy-records in #1356
>修复Sqlite目录带.校验不通过问题 by @maoxian-1 in #1357
>Pr/1344 by @joyqi in #1360
>Fix pgsql reset id error by @sy-records in #1369
>Update admin welcome tip by @sy-records in #1389
>Enhancement of Typecho\Cookie by @sy-records in #1399
>fix CORS issues in preview page. 修复文章预览页面跨域问题 by @Valpha in #1400
>模板缩略图支持识别webp图片后缀 by @jrotty in #1403
>修正注释 by @jrotty in #1411
>Fix notice not clear by @sy-records in #1416
>修复管理员进入其他用户文章列表时显示所有文章的bug by @jrotty in #1415
>Fix QUIC/https Mixed Content by @MBRjun in #1423
>Add admin/footer.php begin plugin by @sy-records in #1426
>Fix missing change themeUrl by @sy-records in #1431
>Fix category creation error when using xmlrpc by @sy-records in #1443
>Fix #1449 by @sy-records in #1450
>Minor update by @vndroid in #1451
>Minor update by @vndroid in #1460
>Fix the error of getting request parameters by @sy-records in #1464
>Fix multiple calls returning the same object (#1412) by @benzBrake in #1478
>Fix use SQLite error of windows install by @sy-records in #1471
>Adjust style of edit comments by @sy-records in #1483
>Fix comments feed jump error by @sy-records in #1491
>Fix #1495 by @sy-records in #1496
>Fix unsafe use of jQuery .html() by @l2dy in #1382
>Fix htmlspecialchars error for feed by @sy-records in #1522
>Use https links by @l2dy in #1280
>Support ssl for pdo_mysql and mysqli by @sy-records in #1525
>Fix: php 8.1 strtolower not allow null value by @benzBrake in #1559
>Fix an XSS vulnerability in v1.2.1-rc by @FaithPatrick in #1561
>fix php 8.1 Deprecated: htmlspecialchars(): Passing null to parameter #1 by @benzBrake in #1570
>Add a prompt message for manual database creation by @sy-records in #1348
>fix #1574 by @joyqi in #1575
>improve release ci, upload built asset after new release published. by @joyqi in #1576
>重复执行判断的优化 by @logdd in #1586

总结:适配PHP8.1,XSS攻击防护优化,其他系统修复级优化
然后，本站因为迁移图片和静态源站分开，然而upyunfile插件500报错，更新需要停止一段时间（用于维护站点文章）
  [1]: https://github.com/typecho/typecho/releases/tag/v1.2.1
