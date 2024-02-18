<?php
error_reporting(0);
$nodeip = '124.221.234.185';	//填写你的服务器IP
$nodetext = 'nuoyis提供技术支持';	//自定义广告*/

if (isset($_GET["msg"]) && $_GET["msg"] != "") {
	$url = addslashes($_GET["msg"]);
	preg_match("/^(\w+:\/\/)?([^\/]+)/i", $url , $matches);  
	// 获得主机名  
	$host = $matches[2];
	if(is_url($host)){
  	//获取当前服务器ip地区
		$node = convertip($nodeip);
	//编码转换
		$nodetext = mb_convert_encoding($nodetext,"UTF-8","GBK");  

		if (PATH_SEPARATOR==':'){	// linux
			exec("ping -c 2 -w 5 $host", $info);
			$strs = reset($info);
			$ping_time_line = end($info);
		  preg_match_all("/\((.*?)\)/",$strs,$str);	//正则首行获取的ip
		  $ip =$str[1][0];
		  if($info[1]!=""){	//正常输出的内容
		  	$ping_time = explode("=", $ping_time_line)[1];
		  	$ping_time_min = explode("/", $ping_time)[0];
		  	$ping_time_avg = explode("/", $ping_time)[1];
		  	$ping_time_max = explode("/", $ping_time)[2];
		  	$location = convertip($ip);
		  	
		  	$arr = "网址：$host\nip地址：$ip\n最小延迟：".$ping_time_min."ms\n最大延迟：".$ping_time_max."ms\n平均延迟：".$ping_time_avg."ms\n节点：$location";
		  	echo "$arr\n注：本司节点位于香港，ping结果仅供参考！";
		  /*	$arr = array("host"=>$host,"ip"=>$ip,"location"=>$location,"ping_time_min"=>$ping_time_min.'ms',"ping_time_avg"=>$ping_time_avg.'ms',"ping_time_max"=>$ping_time_max.'ms',"state"=>"1000","node"=>$node,'nodetext'=>$nodetext);
		    echo json_encode($arr);		//location:域名节点地址,ping_time_min:最小延迟,ping_time_avg:平均延迟,ping_time_max:最大延迟,node:该服务器地区,nodetext:自定义文字*/
		  }elseif(empty($ip)){	//获取不到ip同时获取不到主机，说明当前地址错误或者未解析
		  	error();
		  }else{	//禁Ping时输出的内容
		  	$title = explode(' ', $strs);
		  	$location = convertip($ip);
		  	$arr = "ip：$ip\n节点：$location";
		  	echo "$arr\n";
		  /*	$arr = array("host"=>$host,"ip"=>$ip,"location"=>$location,"state"=>"1002","title"=>$title[1],"node"=>$node,'nodetext'=>$nodetext);
		  	echo json_encode($arr);
		    //location:域名节点地址,title:返回特殊地址,node:该服务器地区,nodetext:自定义文字*/
		  }
		}
		else{						// windows
			exec("ping $host", $info);
			if($info[0]!=''){
				$arr = array("host"=>$host,"state"=>"1003","title"=>"请求找不到主机");
				echo "抱歉，找不到主机";
				exit();
			}
		  //获取ip正则
			$strs = $info[1];
			preg_match_all("/\[(.*?)\]/",$strs,$str);
			$ip =$str[1][0];
		  //获取ping值结果
			$info_time = end($info);
			$target = $info[2];

			$info_times = explode(" ",$info_time);
			$min_time = str_replace("，最长","",$info_times[6]);
			$max_time = str_replace("，平均","",$info_times[8]);
			$avg_time = str_replace("，最长","",$info_times[10]);

		  //判断是否有ping值结果
			$result = checkStr("ms",$info_time);
			if($result){
				$location = convertip($ip);
				$arr = "网址：$host\nip地址：$ip\n最小延迟：".$min_time."ms\n最大延迟：".$max_time."ms\n平均延迟：".$avg_time."ms\n节点：$location";
		  	echo "$arr\n注：本司节点位于香港，ping结果仅供参考！";
				/*$arr = array("host"=>$host,"ip"=>$ip,"location"=>$location,"ping_time_min"=>$min_time,"ping_time_avg"=>$avg_time,"ping_time_max"=>$max_time,"state"=>"1000","node"=>$node,'nodetext'=>$nodetext);
		    echo json_encode($arr);	//location:域名节点地址,ping_time_min:最小延迟,ping_time_avg:平均延迟,ping_time_max:最大延迟,node:该服务器地区,nodetext:自定义文字*/
		  }elseif(empty($ip)){		//获取不到ip同时获取不到主机，说明当前地址错误或者未解析
		  	error();
		  }else{	//禁Ping时输出的内容
		  	$location = convertip($ip);
		  //	$arr = array("host"=>$host,"ip"=>$ip,"location"=>$location,"state"=>"1002","node"=>$node,'nodetext'=>$nodetext);echo json_encode($arr);	//location:域名节点地址,node:该服务器地区,nodetext:自定义文字
		  echo "ip：".$ip."\n节点信息：".$location."\n地址：".$node."";
		}
	}
}else{error();}
}else{error();}



function error(){
	$host = $_GET["msg"];
echo "抱歉，ping出错了。\n原因：未解析或禁ping。";
	exit;
}

function convertip($ip) {
  //纯真IP数据库IP定位
	$dat_path = 'qqwry.dat';
	if(!$fd = @fopen($dat_path, 'rb')){  
		return 'IP数据库文件不存在或者禁止访问或者已经被删除！';  
	}  
	$ip = explode('.', $ip);  
	$ipNum = $ip[0] * 16777216 + $ip[1] * 65536 + $ip[2] * 256 + $ip[3];  
	$DataBegin = fread($fd, 4);  
	$DataEnd = fread($fd, 4);  
	$ipbegin = implode('', unpack('L', $DataBegin));  
	if($ipbegin < 0) $ipbegin += pow(2, 32);  
	$ipend = implode('', unpack('L', $DataEnd));  
	if($ipend < 0) $ipend += pow(2, 32);  
	$ipAllNum = ($ipend - $ipbegin) / 7 + 1;  
	$BeginNum = 0;  
	$EndNum = $ipAllNum;  
	while($ip1num>$ipNum || $ip2num<$ipNum) {  
		$Middle= intval(($EndNum + $BeginNum) / 2);  
		fseek($fd, $ipbegin + 7 * $Middle);  
		$ipData1 = fread($fd, 4);  
		if(strlen($ipData1) < 4) {  
			fclose($fd);  
			return '系统出错！';  
		}  
		$ip1num = implode('', unpack('L', $ipData1));  
		if($ip1num < 0) $ip1num += pow(2, 32);  
		if($ip1num > $ipNum) {  
			$EndNum = $Middle;  
			continue;  
		}  
		$DataSeek = fread($fd, 3);  
		if(strlen($DataSeek) < 3) {  
			fclose($fd);  
			return '系统出错！';  
		}  
		$DataSeek = implode('', unpack('L', $DataSeek.chr(0)));  
		fseek($fd, $DataSeek);  
		$ipData2 = fread($fd, 4);  
		if(strlen($ipData2) < 4) {  
			fclose($fd);  
			return '系统出错！';  
		}  
		$ip2num = implode('', unpack('L', $ipData2));  
		if($ip2num < 0) $ip2num += pow(2, 32);  
		if($ip2num < $ipNum) {  
			if($Middle == $BeginNum) {  
				fclose($fd);  
				return '未知';  
			}  
			$BeginNum = $Middle;  
		}  
	}  
	$ipFlag = fread($fd, 1);  
	if($ipFlag == chr(1)) {  
		$ipSeek = fread($fd, 3);  
		if(strlen($ipSeek) < 3) {  
			fclose($fd);  
			return '系统出错！';  
		}  
		$ipSeek = implode('', unpack('L', $ipSeek.chr(0)));  
		fseek($fd, $ipSeek);  
		$ipFlag = fread($fd, 1);  
	}  
	if($ipFlag == chr(2)) {  
		$AddrSeek = fread($fd, 3);  
		if(strlen($AddrSeek) < 3) {  
			fclose($fd);  
			return '系统出错！';  
		}  
		$ipFlag = fread($fd, 1);  
		if($ipFlag == chr(2)) {  
			$AddrSeek2 = fread($fd, 3);  
			if(strlen($AddrSeek2) < 3) {  
				fclose($fd);  
				return '系统出错！';  
			}  
			$AddrSeek2 = implode('', unpack('L', $AddrSeek2.chr(0)));  
			fseek($fd, $AddrSeek2);  
		} else {  
			fseek($fd, -1, SEEK_CUR);  
		}  
		while(($char = fread($fd, 1)) != chr(0))  
			$ipAddr2 .= $char;  
		$AddrSeek = implode('', unpack('L', $AddrSeek.chr(0)));  
		fseek($fd, $AddrSeek);  
		while(($char = fread($fd, 1)) != chr(0))  
			$ipAddr1 .= $char;  
	} else {  
		fseek($fd, -1, SEEK_CUR);  
		while(($char = fread($fd, 1)) != chr(0))  
			$ipAddr1 .= $char;  

		$ipFlag = fread($fd, 1);  
		if($ipFlag == chr(2)) {  
			$AddrSeek2 = fread($fd, 3);  
			if(strlen($AddrSeek2) < 3) {  
				fclose($fd);  
				return '系统出错！';  
			}  
			$AddrSeek2 = implode('', unpack('L', $AddrSeek2.chr(0)));  
			fseek($fd, $AddrSeek2);  
		} else {  
			fseek($fd, -1, SEEK_CUR);  
		}  
		while(($char = fread($fd, 1)) != chr(0)){  
			$ipAddr2 .= $char;  
		}  
	}  
	fclose($fd);  
	if(preg_match('/http/i', $ipAddr2)) {  
		$ipAddr2 = '';  
	}  
	$ipaddr = "$ipAddr1 $ipAddr2";  
	$ipaddr = preg_replace('/CZ88.Net/is', '', $ipaddr);  
	$ipaddr = preg_replace('/^s*/is', '', $ipaddr);  
	$ipaddr = preg_replace('/s*$/is', '', $ipaddr);  
	if(preg_match('/http/i', $ipaddr) || $ipaddr == '') {  
		$ipaddr = '未知';  
	}  
	$ipaddr = iconv('gbk', 'utf-8//IGNORE', $ipaddr);   
	if( $ipaddr != '  ' )  
		return $ipaddr;  
	else 
		$ipaddr = '来自火星，无法或者其所在地!';  
	return $ipaddr;  
}

function checkStr($str,$target){
  	//字符串是否存在正则
	$tmpArr = explode($str,$target);
	if(count($tmpArr)>1)return true;
	else return false;
}


function is_url($str){
	//域名正则
	return preg_match("/^((https?|ftp|news):\/\/)?([a-z]([a-z0-9\-]*[\.。])+([a-z]{2}|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil|museum|name|nato|net|org|pro|travel|vip|xyz)|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))(\/[a-z0-9_\-\.~]+)*(\/([a-z0-9_\-\.]*)(\?[a-z0-9+_\-\.%=&]*)?)?(#[a-z][a-z0-9_]*)?$/", $str);
}

?>