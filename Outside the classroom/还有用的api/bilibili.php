<?php
header("content-Type: text/html; charset=UTF-8");
error_reporting(E_ALL^E_NOTICE^E_WARNING);
$error = $code = $date = '';
if ($_GET['msg'] != null){
    $keywords=urlencode($_GET['msg']);
    $data =file_get_contents("http://app.bilibili.com/x/v2/search?appkey=1d8b6e7d45233436&build=560161&duration=0&keyword=$keywords&mobi_app=android&platform=android&pn=1&ps=10&ts=1534807273&sign=58fec668fa2fb65a5149d04aeca15cbb");
    $c=(json_decode($data,true));
    if($_GET["n"] == null)
    {
        $date = json_encode(liebiao($c));
        $code = 200;
    }
    else
    {
        $date = xuange($c,$_GET["n"]);
        $code = 200;
    }
}else{
    $code = 201;
    $error = '木有参数请重新传入';
}
echo json_encode(array('code' => $code, 'error' => $error, 'data' => $date));

function liebiao($c)
{
$result=$c["data"]["nav"][4]["total"];
$array = array();
for( $i = 0 ; $i < $result && $i < 5 ; $i ++ )

{
$e=$c["data"]["items"]["archive"][$i];
$b=$e["title"];
$mi=$e["author"];
$array[$i] = array('num' => $i+1, 'opus' => $mi, 'up' => $mi);
}
return $array;
}


function xuange($c,$list)
{
$d=$e=$c["data"]["items"]["archive"][($list-1)];
$pic=$d["cover"];
$upzhu=$d["author"];
$jieshao=$d["desc"];
$id=$d["param"];
$time=$d["duration"];
return array('img' => $pic, 'up' => $upzhu, 'about' => $jieshao, 'time' => $time, 'url' => "https://www.bilibili.com/video/av$id");
}
?>