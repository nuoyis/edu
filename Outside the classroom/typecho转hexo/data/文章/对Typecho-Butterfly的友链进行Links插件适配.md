---
title: 对Typecho-Butterfly的友链进行Links插件适配
date: 2023-06-12 11:11:00
categories: 技术类
tags: []
---

>error-codes));
         }
     }        
    }
}
return $comment;
}

// 微博热搜
function weibohot(){
$api = file_get_contents('https://weibo.com/ajax/side/hotSearch');
$data = json_decode($api,true)['data']['realtime'];

$jyzy = array(
	'电影' => '影',
	'剧集' => '剧',
	'综艺' => '综',
	'音乐' => '音',
	'盛典' => '盛',
);

$hotness = array(
    '爆' => 'weibo-boom',
    '热' => 'weibo-hot',
    '沸' => 'weibo-boil',
    '新' => 'weibo-new',
    '荐' => 'weibo-recommend',
    '音' => 'weibo-jyzy',
    '影' => 'weibo-jyzy',
    '剧' => 'weibo-jyzy',
    '综' => 'weibo-jyzy',
    '盛' => 'weibo-jyzy',
    );

foreach($data as $item){
	$hot = '荐';
	if(isset($item['is_ad'])){
		continue;
	}
	if(isset($item['is_boom'])){
		$hot = '爆';
	}
	if(isset($item['is_hot'])){
		$hot = '热';
	}
	if(isset($item['is_fei'])){
		$hot = '沸';
	}
	if(isset($item['is_new'])){
		$hot = '新';
	}e
	if(isset($item['flag_desc'])){
		$hot = $jyzy[$item['flag_desc']];
	}
	echo '<div class="weibo-list-item"><div class="weibo-hotness '.$hotness[$hot].'">'.$hot.'</div><span class="weibo-title"><a title="'.$item['note'].'" href="https://s.weibo.com/weibo?q=%23' . $item['word'] . '%23" target="_blank" rel="external nofollow noreferrer" style="color:#a08ed5">'.$item['note'].'</a></span><div class="weibo-num"><span>'.$item['num'].'</span></div></div>';
    }
}
```
修改完上面的内容后，需要外观设置成插件模式，然后下载links插件。

常见问题
1.为什么不显示
首先检查是否独立页面创建相关模板页面，如下图所设置
![独立页面检查][6]


  [1]: https://io.nuoyis.net/typecho/uploads/2023/06/4176718260.webp
  [2]: https://io.nuoyis.net/typecho/uploads/2023/06/2529222940.webp
  [3]: https://io.nuoyis.net/typecho/uploads/2023/06/2415076383.webp
  [4]: https://io.nuoyis.net/typecho/uploads/2023/06/2415076383.webp
  [5]: https://io.nuoyis.net/typecho/uploads/2023/06/2415076383.webp
  [6]: https://io.nuoyis.net/typecho/uploads/2023/06/2415076383.webp
