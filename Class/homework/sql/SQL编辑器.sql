use xk;
/*1查询林斌同学选修的课程的课程号，志愿号，同时还要显示该同学的学号，要求按照志愿号升序排序*/
select Stuno,couno,willorder
from stucou
where stuno in
(
select stuno
from student
where stuname = '林斌'
)
order by willorder;

/*2 查询建筑工程系的全部班级的班号和班名*/
/*外层 class 内层:department 公共列:departno*/
select ClassNo,classname
from class
where DepartNo in
(
select DepartNo
from department
where DepartName = '建筑工程系'
);
/*3查询世界旅游这门课程的报名状态，要求显示课号，报名状态*/
/*内层:course 外层:stucou 公共列:couno*/
select CouNo, State
from stucou
where CouNo in
(
select CouNo
from course
where CouName = '世界旅游'
);
/*4查询李韵婷老师所在的系的系号和系名*/
/*外层 */
select DepartNo,DepartName
from department
where DepartNo in
(
select DepartNo
from course
where Teacher = '李韵婷'
);
/*5统计房地产漫谈这门课，一共有多少个条报名记录*/
/*外层:stucou 内层:course 公共列:couno*/
select count(*) as 报名记录总数
from stucou
where couno in
(
select couno
from course
where couname = '房地产漫谈'
);
select sum(WillOrder)
from stucou
where CouNo in
(
select CouNo
from course
where CouName = '房地产漫谈'
);
/*6统计旅游系开设的所有课程的总报名人数和总限选人数*/
select sum(willnum) as 总报名人数,
       sum(limitnum) as 总限选人数
from course
where departno in
(
select departno
from department
where departname = '旅游系'
);
/*7请分别统计旅游系和计算机应用工程系各自开设的课程的总门数*/
/* 外层:course 内层: departno 公共列:departno
分组标准:departno*/
select departno,count(*) as 该系的课程总门数
from course
where departno in
(
select departno
from department
where departname in ('旅游系','计算机应用工程系')
)
group by departno;

/*多表连接查询:内连接和外连接
内连接:只保留满足连接条件的数据行的连接*/

/*交叉连接：笛卡尔积 考勤场景
交叉连接把1张表的所有数据行，依次与另一张表的所有数据行直接连接，产生所有排列组合
很多数据行是没有意义的*/

/*嵌套查询 与 多表连接查询 的关系
大多数的嵌套查询，可以使用多表连接查询替代的。
输出列，来自于1张表，可以使用嵌套查询
输出列，来自于2张或更多表，只能多表连接。
输出，筛选条件包含聚合函数(但无分组)
都来自1张表，拿一个子查询去包裹聚合函数
涉及到较多表的时候，推荐使用多表连接 */
/* 1 查询学生表和班级表的交叉连接的结果*/
select *
from class cross join student;
/*内连接查询：两种写法，通用
               表的数量较多时，推荐 非join on 写法
外连接:必须要用join on
*/
/* 2 查询学生基本信息以及学生所在的班级信息*/
select *
from class join student
on class.classno = student.classno;


select *
from class,student
where class.classno = student.classno;

/*3 查询学生基本信息，班级名称*/
select student.*,classname
from class join student
on class.classno = student.classno;

/*4 查询学生的选课信息，要求显示 学号，姓名，课号,课名，志愿号
要求安卓学号升序排序，学号相同时，按照志愿号升序

哪几张表：stucou student course
公共列的指代，一定要带表名构成的前缀 */
select stucou.stuno,stuname,
       stucou.couno,couname,willorder
from stucou,student,course
where stucou.couno = course.couno
      and
      stucou.stuno = student.stuno
order by stucou.stuno,willorder;

select stucou.stuno,stuname,
       stucou.couno,couname,willorder
from stucou join course
on stucou.couno = course.couno
join student
on stucou.stuno = student.stuno
order by stucou.stuno,willorder;

/* 5 查询 学生报名了"计算机应用工程系"开设的选修课的情况显示：学生姓名，课名，系名
多张表：stucou,department student,course
公共列: department ---course ： departno
        student ---stucou ---course
*/
select stuname,couname,departname
from stucou,student,course,department
where stucou.stuno = student.stuno
      and
      stucou.couno = course.couno
      and
      course.departno = department.departno
      and
      departname = '计算机应用工程系';
      
select stuname,couname,departname
from department join course
on department.departno = course.departno
join stucou
on course.couno = stucou.couno
join student
on stucou.stuno = student.stuno
where departname = '计算机应用工程系';

/* 6 查看 00电子商务班的同学
选修计算机应用工程系开发的选修课的情况，
要求显示 班名，姓名，课名，课所在的系的名称
多张表：department --course
         student - stucou -course
         student -class
*/
select classname,stuname,couname,departname
from department,student,stucou,course,class
where department.departno = course.departno
      and
      stucou.couno = course.couno
      and
      stucou.stuno = student.stuno
      and
      student.classno = class.classno
      and
      departname = '计算机应用工程系'
      and
      classname = '00电子商务';
      
/* 7 查询 计算机应用工程系的同学选修课程的情况
显示：系名（人在的系，不是课所在的系），姓名，课名*/
/*student -- stucou -- course
  department -class -student*/
select departname,stuname,couname
from department,class,student,stucou,course
where department.departno = class.departno
      and
      class.classno = student.classno
      and
      student.stuno = stucou.stuno
      and
      course.couno = stucou.couno
      and
      departname = '计算机应用工程系';

/* 8 计算机系的人，选了计算机系的课，显示：
人所在的系名，姓名，课名，课所在的系的系名
6张表:department 取别名 复制 系表 有2张*/
select d2.departname as 人所在的系名,
       stuname,couname,
       d2.departname as 课所在的系名
from department d1,department d2,
      class,student,stucou,course
where d1.departno = course.departno
      and
      stucou.couno = course.couno
      and
      stucou.stuno = student.stuno
      and
      d2.departno = class.departno
      and
      class.classno = student.classno
      and
      d1.departname = '计算机应用工程系'
      and
      d2.departname = '计算机应用工程系';
