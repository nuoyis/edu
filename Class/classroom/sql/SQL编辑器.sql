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
状态数越少，状态与状态之间，就越不容易混淆 */


