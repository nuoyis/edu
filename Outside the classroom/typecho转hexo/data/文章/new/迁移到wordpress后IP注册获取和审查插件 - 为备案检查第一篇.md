---
title: 迁移到wordpress后IP注册获取和审查插件 - 为备案检查第一篇
date: 2023-02-16 05:54:00
categories: uncategorized
tags: []
---

>query_orderby = "ORDER BY user_registered ".$_REQUEST['order']."";
    }
  }
}

add_action('user_register', 'log_ip');
add_action( 'wp_login', 'k_insert_user_last_login' );
add_action( 'pre_user_query', 'ks_users_search_order' );
add_filter('manage_users_columns', 'k_add_user_additional_column');
add_filter( "manage_users_sortable_columns", 'Ks_users_sortable_columns' );
add_action('manage_users_custom_column',  'k_show_user_additional_column_content', 10, 3);
?>
```

复制代码后桌面上创建PHP后缀名称,且重命名为themepark\_user\_ip.php 感谢你的观看,谢谢
