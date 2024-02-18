<?php
header("Content-Type: text/html;charset=utf-8");
echo base64_decode($_GET["msg"]);
?>