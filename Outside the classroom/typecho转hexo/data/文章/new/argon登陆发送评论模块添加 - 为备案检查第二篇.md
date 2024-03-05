---
title: argon登陆发送评论模块添加 - 为备案检查第二篇
date: 2023-02-18 16:42:00
categories: 技术类
tags: []
---

> user_email);} else {echo htmlspecialchars($current_commenter['comment_author_email']);} ?>">
                        </div>
                    </div>
                </div>
                <div class="<?php echo $col3_class;?>">
                    <div class="form-group">
                        <div class="input-group input-group-alternative mb-4 post-comment-captcha-container" captcha="<?php echo get_comment_captcha(get_comment_captcha_seed());?>">
                            <div class="input-group-prepend">
                                <span class="input-group-text"><i class="fa fa-key"></i></span>
                            </div>
                            <input id="post_comment_captcha" class="form-control" placeholder="<?php _e('验证码', 'argon');?>" type="text" <?php if (current_user_can('level_7')) {echo('value="' . get_comment_captcha_answer(get_comment_captcha_seed()) . '" disabled');}?>>
                            <style>
                                .post-comment-captcha-container:before{
                                    content: attr(captcha);
                                }
                            </style>
                            <?php if (get_option('argon_get_captcha_by_ajax', 'false') == 'true') {?>
                                <script>
                                    $(".post-comment-captcha-container").attr("captcha", "Loading...");
                                    $.ajax({
                                        url : argonConfig.wp_path + "wp-admin/admin-ajax.php",
                                        type : "POST",
                                        dataType : "json",
                                        data : {
                                            action: "get_captcha",
                                        },
                                        success : function(result){
                                            $(".post-comment-captcha-container").attr("captcha", result['captcha']);
                                        },
                                        error : function(xhr){
                                            $(".post-comment-captcha-container").attr("captcha", "<?php _e('获取验证码失败', 'argon');?>");
                                        }
                                    });
                                </script>
                            <?php } ?>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row hide-on-comment-editing" id="post_comment_extra_input" style="display: none";>
                <div class="col-md-12" style="margin-bottom: -10px;">
                    <div class="form-group">
                        <div class="input-group input-group-alternative mb-4 post-comment-link-container">
                            <div class="input-group-prepend">
                                <span class="input-group-text"><i class="fa fa-link"></i></span>
                            </div>
                            <input id="post_comment_link" class="form-control" placeholder="<?php _e('网站', 'argon'); ?>" type="text" name="url" value="<?php echo htmlspecialchars($current_commenter['comment_author_url']); ?>">
                        </div>
                    </div>
                </div>
            </div>
            <div class="row hide-on-comment-editing <?php if (get_option('argon_hide_name_email_site_input') == 'true') {echo 'd-none';}?>" style="margin-top: 10px; <?php if (is_user_logged_in()) {echo('display: none');}?>">
                <div class="col-md-12">
                    <button id="post_comment_toggle_extra_input" type="button" class="btn btn-icon btn-outline-primary btn-sm" tooltip-show-extra-field="<?php _e('展开附加字段', 'argon'); ?>" tooltip-hide-extra-field="<?php _e('折叠附加字段', 'argon'); ?>">
                        <span class="btn-inner--icon"><i class="fa fa-angle-down"></i></span>
                    </button>
                </div></div>
            <div class="row" style="margin-top: 5px; margin-bottom: 10px;">
                <div class="col-md-12">
                    <?php if (get_option("argon_comment_allow_markdown") != "false") {?>
                        <div class="custom-control custom-checkbox comment-post-checkbox comment-post-use-markdown">
                            <input class="custom-control-input" id="comment_post_use_markdown" type="checkbox" checked="true">
                            <label class="custom-control-label" for="comment_post_use_markdown">Markdown</label>
                        </div>
                    <?php } ?>
                    <?php if (get_option("argon_comment_allow_privatemode") == "true") {?>
                        <div class="custom-control custom-checkbox comment-post-checkbox comment-post-privatemode" tooltip="<?php _e('评论仅发送者和博主可见', 'argon'); ?>">
                            <input class="custom-control-input" id="comment_post_privatemode" type="checkbox">
                            <label class="custom-control-label" for="comment_post_privatemode"><?php _e('悄悄话', 'argon');?></label>
                        </div>
                    <?php } ?>
                    <?php if (get_option("argon_comment_allow_mailnotice") == "true") {?>
                        <div class="custom-control custom-checkbox comment-post-checkbox comment-post-mailnotice" tooltip="<?php _e('有回复时邮件通知我', 'argon'); ?>">
                            <input class="custom-control-input" id="comment_post_mailnotice" type="checkbox"<?php if (get_option("argon_comment_mailnotice_checkbox_checked") == 'true'){echo ' checked';}?>>
                            <label class="custom-control-label" for="comment_post_mailnotice"><?php _e('邮件提醒', 'argon');?></label>
                        </div>
                    <?php } ?>
                    <button id="post_comment_send" class="btn btn-icon btn-primary comment-btn pull-right mr-0" type="button">
                        <span class="btn-inner--icon hide-on-comment-editing"><i class="fa fa-send"></i></span>
                        <span class="btn-inner--icon hide-on-comment-not-editing"><i class="fa fa-pencil"></i></span>
                        <span class="btn-inner--text hide-on-comment-editing" style="margin-right: 0;"><?php _e('发送', 'argon');?></span>
                        <span class="btn-inner--text hide-on-comment-not-editing" style="margin-right: 0;"><?php _e('编辑', 'argon');?></span>
                    </button>
                    <button id="post_comment_edit_cancel" class="btn btn-icon btn-danger comment-btn pull-right hide-on-comment-not-editing" type="button" style="margin-right: 8px;">
                        <span class="btn-inner--icon"><i class="fa fa-close"></i></span>
                        <span class="btn-inner--text"><?php _e('取消', 'argon');?></span>
                    </button>
                    <?php if (get_option("argon_comment_emotion_keyboard", "true") != "false"){ ?>
                        <button id="comment_emotion_btn" class="btn btn-icon btn-primary pull-right" type="button" title="<?php _e('表情', 'argon');?>">
                            <i class="fa fa-smile-o" aria-hidden="true"></i>
                        </button>
                        <?php get_template_part( 'template-parts/emotion-keyboard' ); ?>

                    <?php } ?>
                </div>
            </div>
            <input id="post_comment_captcha_seed" value="<?php echo $commentCaptchaSeed;?>" style="display: none;"></input>
            <input id="post_comment_post_id" value="<?php echo get_the_ID();?>" style="display: none;"></input>
        </form>
    </div>
</div>
<div id="comment_edit_history" class="modal fade" tabindex="-1" role="dialog" aria-modal="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title" style="font-size: 20px;"></h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body" style="word-break: break-word;"></div>
        </div>
    </div>
</div>
<div id="comment_pin_comfirm_dialog" class="modal fade" tabindex="-1" role="dialog" aria-modal="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title" style="font-size: 20px;"></h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body" style="word-break: break-word;"></div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary btn-dismiss" data-dismiss="modal"></button>
                <button type="button" class="btn btn-primary btn-comfirm"></button>
            </div>
        </div>
    </div>
</div>
<?php endif; ?>
<?php } ?>
```

目前代码已经提交至主题,链接:[https://github.com/solstice23/argon-theme/issues/593](https://github.com/solstice23/argon-theme/issues/593)
