select *
from course
order by convert(teacher using gbk);
/*算数运算*/
select 5+6,5-6,5*6,5/6,5%6;
/*比较运算符
查询 报名人数小于等于25， 大于等于15 的课程信息
注意：怎么念，怎么敲；符号间没有空格的。
*/
select *
from course
where willnum >= 15 and willnum <= 25;

/*between 小数值 and 大数值。颠倒大小顺序，不对*/
select *
from course
where willnum between 15 and 25;

/*查询 表明人数要么大于25，要么小于15的课程信息*/
select *
from course
where willnum not between 15 and 25;

select *
from course
where willnum >25 or willnum < 15;

/*查询 课程编号为001 004 007 017 018 的课程名称 课程号*/
select couno,couname
from course
where couno in ('001', '004', '007', '017', '018');

/*查询 课程编号不为001 004 007 017 018 的课程名称 课程号*/
select couno,couname
from course
where couno not in ('001', '004', '007', '017', '018');

/* 位运算符： 针对二进制数的运算。
M进制:有M个状态；
状态数越少，状态与状态之间，就越不容易混淆
抗干扰能力更强 更可靠

状态个数越多，单个状态携带的信息量大 */
select bin(3), bin(6), 3&6, bin(3&6), bin(3|6) ;
/*     3: 11s
       6: 110
按位与    010 
       7: 111
       3: 11
       6: 110
按位或    111         */

/*左移 右移 显示 7 按位右移2位的结果*/
select bin(7), bin(7>>2);
/*右移2位 111 变成 1
左移2位 111 变成 11100*/

/*排序： 1 排序代码最后
         2 排序的代码，只需要1句
         3 在这一句排序代码中，可以有多个排序标准的
         4 中文可以排序，可能需要convert函数，转一下编码规则
         编码规则：人类语言字符-----01编码
         常见的编码规则: utf-8-sig 通用的，包含几乎所有人类语言字符 gbk,gbk2312*/

/*查询课程信息，安装报名人数 升序排序*/
select *
from course
order by willnum desc;

/*查询课程信息
结果先按学分升序，当学分相同时，按照课程编号升序排列*/
select *
from course
order by credit,couno;

/*中文排序: 查看课程信息，要求按照教师姓名，升序*/
select *
from course
order by convert(teacher using gbk);

/*查询 课表的课程信息，显示报名人数与限选人数之比*/
select *,willnum/limitnum
from course;

/* 替换查询结果中的列值: 具备扩展功能的，好用在课程表中，查询课程名称，学分。
如果，学分=1，显示 每两周上2节课                       
学分=2，显示 每周上2节课
学分=3，显示 每周上3节课
否则 显示 待定 */
select couname,credit,
       case
           when credit=1.0 then '每两周上2节课'
           when credit=2.0 then '每周上2节课'
           when credit=3.0 then '每周上3节课'
           else '待定'
       end as '安排'
from course;