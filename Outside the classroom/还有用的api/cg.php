<?php
$msg = $_GET['msg'];
$b = $_GET['n'];
$str = "http://api.ring.kugou.com/ring/search?q=".$_GET["msg"]."&t=3&subtype=1&p=1&pn=200&st=2";
$str=file_get_contents($str);
function replace_unicode_escape_sequence($match) {
  return mb_convert_encoding(pack('H*', $match[1]), 'UTF-8', 'UCS-2BE');}
$str = preg_replace_callback('/\\\\u([0-9a-f]{4})/i', 'replace_unicode_escape_sequence', $str);
$stre = '/"singerName": "(.*?)"(.*?)"ringName": "(.*?)"(.*?)"url": "(.*?)"/'; 
$result = preg_match_all($stre,$str,$trstr);
if($result== 0){
echo "搜索不到与".$_GET['msg']."的相关歌曲，请稍后重试或换个关键词试试。";
}else{
if($b== null){
for( $i = 1 ; $i < $result && $i < 11 ; $i ++ )
{
$ga=$trstr[3][$i];//获取歌名
$gb=$trstr[1][$i];//获取歌手
echo ($i)."：".$ga."--".$gb."\n";
}
echo "\n共搜索到与".$_GET['msg']."的相关歌曲".$result."条，您可以点1～".$result."任一曲。";
}
else
{
//
$i=($b);
$l=$trstr[5][$i];
$ga=$trstr[3][$i];//获取歌名
$gb=$trstr[1][$i];//获取歌手
if(!$l == ' '){
die ('列表中暂无序号为『'.$b.'』的歌。');
}
echo $l;
//echo "\$群语音 ".$l."$";
//echo "\$发送 群 ptt %群号% -1 ".$l."\$";
}
}

?>