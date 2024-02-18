<?php
header("content-Type: text/html; charset=UTF-8");
$b = $_GET['n'];
$name = $_GET['msg'];
$array=array("说明" => "待添加");
$from=$array[$name];
if($from!=""){echo $from;}else{
$str = "https://m.douyu.com/api/search/getData?sk=".$name."&type=1&sort=1&limit=20&offset=0"; 
$str=file_get_contents($str);
preg_match_all('/"live":\[(.*?)]}/',$str,$str);
$str=$str[1][0];
$stre = '/{"roomId":(.*?),"vipId":(.*?),"nickname":"(.*?)","roomName":"(.*?)","roomSrc":"(.*?)","hn":"(.*?)","isLive":(.*?),"isVertical":(.*?),"cate2Id":(.*?),"cateName":"(.*?)"}/'; 

$result = preg_match_all($stre,$str,$trstr);
if($result== 0){
echo "搜索不到与".$name."的相关直播，请稍后重试或换个关键词试试。";
}else{
if($b== null){
for( $i = 0 ; $i < $result && $i < 10 ; $i ++ ){
$ga=$trstr[3][$i];//直播间
$gb=$trstr[6][$i];//介绍
echo ($i+1)."：".$ga."--".$gb."人观看\r";}
echo "\n搜索到与".$name."相关的直播信息共".$result."条，您可以点1～".$result."任一直播间，当观看数为零时，主播可能已下播。";}else{
$i=($b-1);
$ga=$trstr[3][$i];//直播间
$gb=$trstr[4][$i];//介绍
$b1=$trstr[6][$i];//热度
$a=$trstr[5][$i];//图片链接
$b=$trstr[1][$i];//id
$x=file_get_contents("https://m.douyu.com/".$b."");
preg_match_all('/notice":"(.*?)"/',$x,$x);
$j=$x[1][0];
              if(!$b == ' '){
die ('列表中暂无序号为『'.$b.'』的直播间，请输入存在的序号进行搜索。');
}
echo "±","img=";
echo "".$a."±";
//判断直播是否进行
if($b1== 0){

echo "直播间：".$ga."\n介绍：".$gb."  ".$j."\n直播链接：https://m.douyu.com/".$b."\n当前主播不在线，您可以观看直播回放。";

}else{
echo "直播间：".$ga."\n介绍：".$gb."  ".$j."\n直播链接：https://m.douyu.com/".$b."\n".$b1."人正在观看";}
}}
}
?>