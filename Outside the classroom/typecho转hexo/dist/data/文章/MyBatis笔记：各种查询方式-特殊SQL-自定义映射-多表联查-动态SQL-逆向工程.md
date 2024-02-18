---
title: MyBatis笔记：各种查询方式-特殊SQL-自定义映射-多表联查-动态SQL-逆向工程
date: 2023-08-22 19:20:00
categories: MyBatis
tags: [MyBatis,特殊SQL,动态SQL,自定义映射,多表联查,逆向工程,分页插件]
---
MyBatis笔记：各种查询功能,特殊SQL语句，动态SQL语句，MyBatis中的一二级缓存，清新版和奢华版的逆向工程的使用，包括我自己的对于多表联查的视频解释，分页查询的插件，还有我对于报错的问题解决思路。篇幅较长，可以选择所需查看。


<!--more-->

##各种查询方式
###查询单条信息/多条信息

SelectMapper接口
```java
public interface SelectMapper {
    /*
    根据id来查询用户信息/返回值可以使用User或者是List<User>
    */
    public abstract List<User> getUserById(@Param("id") Integer id);


    /*
    查询所有的用户信息
    */
    public abstract List<User> getAllUser();

}
```

SelectMapper.xml
```xml
    <!--User getUserById(@Param("id") Integer id);-->
    <select id="getUserById" resultType="User">
        select * from t_user where id = #{id}
    </select>

    <!--List<User> getAllUser();-->
    <select id="getAllUser" resultType="User">
        select * from t_user
    </select>
```
测试类

```java
public class SelectMapperTest {
    /**
     * MyBatis的各种查询功能
     * 1.若查询出的数据只有一条，
     * a>可以通过实体类对象
     * b>可以通过List集合接收
     * c>可以通过Map集合接收
     *
     * 2.若查询出的数据有多条，
     * a>可以通过List集合接收
     * b>可以通过Map集合接收
     *注意：一定不能通过实体类对象来接收，此时会抛异常TooManyResultsException
     * */
    @Test
    public void testGetAllUser(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        //查询所有的用户信息
        System.out.println("user = " + mapper.getAllUser());
    }

    @Test
    public void testGetUserById(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        //查询用户id为3的用户信息
        System.out.println("user = " + mapper.getUserById(3));
    }

}
```
###使用聚合函数查询单行信息

SelectMapper接口
```java
   /*
    查询用户信息的总记录数
    */
    public abstract Integer getCount();
```

SelectMapper.xml
```xml
    <!--Integer getCount();-->
    <!--resultType中一定要想好些什么内容，作为查询的结果返回。
    mybatis默认设置了类型别名不区分大小写; int/_int/Integer/integer/全类名-->
    <select id="getCount" resultType="java.lang.Integer">
        select count(*) from t_user
    </select>
```
###查询用户信息为Map集合
我们可以把查询出来的结果转换为一个map集合，以字段为键，字段对应的值为值。

####查询单条数据为Map集合

SelectMapper接口
```java
    /*
    根据id查询用户信息为一个map集合
    */
    public abstract Map<String, Object> getUserByIdToMap(@Param("id") Integer id);
```
SelectMapper.xml

```xml
    <!--Map<String, Object> getUserByIdToMap(@Param("id") Integer id);-->
    <select id="getUserByIdToMap" resultType="map">
        select * from t_user where id = #{id}
    </select>
```
####查询多条数据为Map集合
 - 把map集合放入List集合中
需要调整返回值，把多条数据的返回值放到一个List集合中，每一条转换的map放到了List集合中
 - 在接口方法上添加@MapKey注解
 [label color="red"]@MapKey设置当前map集合的键，会把我们查询出来数据的某一个字段作为键(唯一)，查询出来数据的map集合作为值[/label] 

SelectMapper接口
```java
    /*
    查询所有用户信息为map集合
    */
    //public abstract List<Map<String, Object>> getAllUserToMap();
    @MapKey("id")
    public abstract Map<String, Object> getAllUserToMap();
```
SelectMapper.xml

```xml
    <!--Map<String, Object> getAllUserToMap();-->
    <select id="getAllUserToMap" resultType="map">
        select * from t_user
    </select>

```
测试类最终源码
SelectMapperTest
```java
public class SelectMapperTest {
    /**
     * MyBatis的各种查询功能
     * 1.若查询出的数据只有一条，
     * a>可以通过实体类对象
     * b>可以通过List集合接收
     * c>可以通过Map集合接收
     *结果：Map = {password=123456, sex=男, id=3, age=23, email=12345@qq.com, username=admin}
     *
     * 2.若查询出的数据有多条，
     * a>可以通过实体类类型的List集合接收
     * b>可以通过map类型的Map集合接收
     * c>可以在mapper接口方法上添加@MapKey注解，
     * 此时就可以将每条数据转换的map集合作为值，以某个字段的值作为键，放在同一个map集合中
     *注意：一定不能通过实体类对象来接收，此时会抛异常TooManyResultsException
     *
     * MyBatis中设置了默认的类型别名
     * Java.lang.Integer  -->int,Integer
     * int --> _int,integer
     * Map --> map
     * String -->string
     * */
    @Test
    public void testGetALLUserToMap(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        System.out.println("Map = " + mapper.getAllUserToMap());
    }

    @Test
    public void testGetUserByIdToMap(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        //查询id为3的用户信息的map集合
        System.out.println("Map = " + mapper.getUserByIdToMap(3));
    }

    @Test
    public void testGetCount(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        //查询所有的用户信息
        System.out.println("Count = " + mapper.getCount());
    }

    @Test
    public void testGetAllUser(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        //查询所有的用户信息
        System.out.println("user = " + mapper.getAllUser());
    }

    @Test
    public void testGetUserById(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        SelectMapper mapper = sqlSession.getMapper(SelectMapper.class);
        //查询用户id为3的用户信息
        System.out.println("user = " + mapper.getUserById(3));
    }

}

```
SelectMapper接口
```java
public interface SelectMapper {
    /*
    根据id来查询用户信息/返回值可以使用User或者是List<User>
    */
    public abstract List<User> getUserById(@Param("id") Integer id);


    /*
    查询所有的用户信息
    */
    public abstract List<User> getAllUser();

    /*
    查询用户信息的总记录数
    */
    public abstract Integer getCount();

    /*
    根据id查询用户信息为一个map集合
    */
    public abstract Map<String, Object> getUserByIdToMap(@Param("id") Integer id);

    /*
    查询所有用户信息为map集合
    */
    //public abstract List<Map<String, Object>> getAllUserToMap();
    @MapKey("id")
    public abstract Map<String, Object> getAllUserToMap();

}

```
SelectMapper.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!--命名空间namespace和某一个接口的全类名保持一致-->
<mapper namespace="com.atguigu.mybatis.mapper.SelectMapper">
    <!--添加SQL语句，和接口中的方法对应-->
    <!--User getUserById(@Param("id") Integer id);-->
    <select id="getUserById" resultType="User">
        select * from t_user where id = #{id}
    </select>

    <!--List<User> getAllUser();-->
    <select id="getAllUser" resultType="User">
        select * from t_user
    </select>

    <!--Integer getCount();-->
    <!--resultType中一定要想好些什么内容，作为查询的结果返回。
    mybatis默认设置了类型别名不区分大小写; int/_int/Integer/integer/全类名-->
    <select id="getCount" resultType="java.lang.Integer">
        select count(*) from t_user
    </select>

    <!--Map<String, Object> getUserByIdToMap(@Param("id") Integer id);-->
    <select id="getUserByIdToMap" resultType="map">
        select * from t_user where id = #{id}
    </select>

    <!--Map<String, Object> getAllUserToMap();-->
    <select id="getAllUserToMap" resultType="map">
        select * from t_user
    </select>

</mapper>
```

----------
##特殊SQL的执行
能用#{}绝对不使用${}，以下情况使用#{}将会出现一定问题。
###处理模糊查询
处理模糊查询如果使用之前的方式可能会出现一些问题。
![1.png][1]
这时候有两种方式解决

 - 使用**${}**
 `select * from t_user where username like '%${username}%'` 
 - 依然使用**#{}**，只不过写SQL语句要用到 [label color="blue"]字符串拼接concat[/label] 
 `select * from t_user where username like concat('%',#{username},'%')` 
 - 依然使用**#{}**,只不过在%两边加**双引号** [label color="red"]\(最常用\)[/label] 
 `select * from  t_user where username like "%"#{username}"%"` 
![2.png][2]

----------
###批量删除
在使用批量删除的语句中， `delete from t_user where id in ()` 括号中无法使用**#{}**，因为#{}会自动解析出来多一对**单引号**，SQL语句语法格式不对无法实现批量删除，而只能使用**${}**来获取参数。
SQLMapper.xml
```xml
    <!--int deleteMore(@Param("ids") String ids);-->
    <delete id="deleteMore">
        delete from t_user where id in (${ids})
    </delete>
```
###动态设置表名
对于动态设置表名，只能是**${}**来获取参数

```xml
    <!-- List<User> getUserByTableName(@Param("tableName") String tableName);-->
    <select id="getUserByTableName" resultType="User">
        select * from ${tableName}
    </select>
```
![3.png][3]

----------
###添加功能获取自增的主键
场景：如果有一个一对多的表关系，有一个班级表，有一个学生表。一个班级有多个学生，班级对应学生应该是一对多的关系，一对多和多对一都要把表设置在多的一方，我们需要把学生表中设置班级的id。我们可以为某个班级分配学生，就是为我们的学生设置班级，我们需要在**中间获取当前添加班级的id**，才能为班级分配学生。

JDBC中本身就有这样的功能，来获取添加自增的主键，[JDBC中的主键回显][4]
而mybatis中也可以实现

```xml
    <!--void insertUser(User user);获取添加后自动递增的主键、
    useGeneratedKeys：设置当前标签中的sql使用了自增的id
    useGeneratedKeys="true"表示该标签使用了自动递增
    由于增删改返回值固定，即受印象的行数，那么我们只能把自动递增的id，放在我们传输的参数的某一个属性中
    keyProperty：将自增的主键的值赋值给传输到映射文件中参数的某个属性
    -->
    <insert id="insertUser" useGeneratedKeys="true" keyProperty="id">
        insert into t_user values (null,#{username},#{password},#{age},#{sex},#{email})
    </insert>
```
![4.png][5]

----------
##自定义映射resultMap
之前实现查询功能，使用resultType，默认映射关系，要求字段名和属性名一致。把我们查询出来对应的字段名为属性赋值，如果当前**字段名**和**属性名** [label color="red"]不一致[/label] ，或者是**多对一**、**一对多**的关系就需要使用**resultMap**。
java中属性名遵循驼峰命名，MySQL中习惯以_分隔。如果字段名和属性名不一致，如果不改变命名的前提下，解决字段名和属性名不一致有三种方式。
场景：有一个员工表和一个部门表，员工表中有一个部门id对应一个部门表中的部门id，产生了多对一和一对多

 1. 在编写SQL语句时使用**别名**的形式，查询出来的字段名和属性名一致，就可以正常赋值。
EmpMapper.xml
```xml
    <!--List<Emp> getAllEmp();-->
    <select id="getAllEmp" resultType="Emp">
        select eid,emp_name empName,age,sex,email from t_emp
    </select>

```

 2. 添加全局配置[font size="16" color="#240a40"]mapUnderscoreToCamelCase[/font]

mybatis-config.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--引入对应配置文件properties-->
    <properties resource="jdbc.properties"/>

    <!--设置MyBatis的全局配置-->
    <settings>
        <!--将下划线自动映射为驼峰,emp_name : empName -->
        <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>

    <!--以包为单位添加类型别名-->
    <typeAliases>
        <package name="com.atguigu.mybatis.pojo"/>
    </typeAliases>
    <!--连接数据库的环境-->
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>
    </environments>
    <!--以包为单位映入映射文件-->
    <mappers>
        <package name="com.atguigu.mybatis.mapper"/>
    </mappers>
</configuration>
```
EmpMapper.xml
```xml
    <!--List<Emp> getAllEmp();-->
    <select id="getAllEmp" resultType="Emp">
        <!--select eid,emp_name empName,age,sex,email from t_emp-->
        select * from t_emp
    </select>

```

 3. 使用resultMap设置自定义映射
EmpMapper.xml

```xml
    <!--
        resultMap:设置自定义映射关系
        id:唯一标识，不能重复
        type:设置映射关系中的实体类类型
        子标签:
        id:设置主键的映射关系
        result:设置普通字段的映射关系
        属性:
        property:设置映射关系中的属性名，必须是type属性所设置的实体类类型中的属性名
        column:设置映射关系中的字段名，必须是sql语句查询出的字段名
    -->
    <resultMap id="empResultMap" type="Emp">
        <id property="eid" column="eid"></id>
        <result property="empName" column="emp_Name"></result>
        <result property="age" column="age"></result>
        <result property="sex" column="sex"></result>
        <result property="email" column="email"></result>
    </resultMap>
```

使用resultMap处理有点麻烦，一般resultMap是来处理一对多和多对一的问题的。

----------
###多对一的映射处理
表和表直接有关系，表所映射的实体类直接也是存在一定的关系。

Emp类
```java
public class Emp {
    private Integer eid;
    //使用驼峰命名
    private String empName;
    private Integer age;
    private String sex;
    private String email;

    //多对一，创建一所对应的对象就可以
    private Dept dept;

```

[font size="16.5" color="#ff0000"]多对一创建一所对应的对象就可以，一对多设置一个集合就可以。[/font]
处理多对一的映射关系也有三种方法

 1. 使用级联属性赋值
EmpMapper.xml

```xml
    <!--处理多对一映射关系方式一：使用级联属性进行赋值-->
    <resultMap id="empAndDeptResultMapOne" type="Emp">
        <id property="eid" column="eid"></id>
        <result property="empName" column="emp_name"></result>
        <result property="age" column="age"></result>
        <result property="sex" column="sex"></result>
        <result property="email" column="email"></result>
        <result property="dept.did" column="did"></result>
        <result property="dept.deptName" column="dept_name"></result>
    </resultMap>
    <!--Emp getEmpAndDempt(@Param("eid") Integer eid);使用多表查询-->
    <select id="getEmpAndDempt" resultMap="empAndDeptResultMapOne">
        select * from t_emp left join t_dept on t_emp.did = t_dept.did where t_emp.eid = #{eid}
    </select>

```

 2. 使用association标签实现
使用association标签处理多对一的关系
EmpMapper.xml
```xml
    <resultMap id="empAndDeptResultMapTwo" type="Emp">
        <id property="eid" column="eid"></id>
        <result property="empName" column="emp_name"></result>
        <result property="age" column="age"></result>
        <result property="sex" column="sex"></result>
        <result property="email" column="email"></result>
        <!--
        association:处理多对一的映射关系
        property:需要来处理多对一映射关系的属性名
        javaType:表示该属性的类型,通过反射获取属性，查询出来的字段值赋值给属性
        把查询出来的dept对象，赋值到的dept属性，得到一个完整的emp对象
        -->
        <association property="dept" javaType="Dept">
            <id property="did" column="did"></id>
            <result property="deptName" column="dept_name"></result>
        </association>
    </resultMap>

    <!--Emp getEmpAndDempt(@Param("eid") Integer eid);使用多表查询-->
    <select id="getEmpAndDempt" resultMap="empAndDeptResultMapTwo">
        select * from t_emp left join t_dept on t_emp.did = t_dept.did where t_emp.eid = #{eid}
    </select>

```

----------
 3. 使用分步查询
我们可以通过多个SQL语句一步步来实现，我们可以先查员工，通过员工的部门id查询部门信息。

我只提供两个xml文件的书写方式，附上视频。
[video title="多对一分步查询 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-22%2002-42-15.mkv " container="beyz03osczc" subtitle=" " poster=" "] [/video]


EmpMapper.xml
```xml
    <resultMap id="empAndDeptByStepResultMap" type="Emp">
        <id property="eid" column="eid"></id>
        <result property="empName" column="emp_name"></result>
        <result property="age" column="age"></result>
        <result property="sex" column="sex"></result>
        <result property="email" column="email"></result>
        <!--
            property:处理实体类中多对一的属性
            select:设置分布查询的sql的唯一标识(namespace.SQLId或maapper接口的全类名.方法名)
            column:设置分布查询的条件
        -->
        <association property="dept"
                     select="com.atguigu.mybatis.mapper.DeptMapper.getEmpAndDeptByStepTwo"
                     column="did"></association>
    </resultMap>
    <!--Emp getEmpAndDeptByStepOne(@Param("eid") Integer eid);
    第一步：查询员工信息
    -->
    <select id="getEmpAndDeptByStepOne" resultMap="empAndDeptByStepResultMap">
        select * from t_emp where eid = #{eid}
    </select>
```

DeptMapper.xml
```xml
    <!--Dept getEmpAndDeptByStepTwo(@Param("did") Integer did);-->

    <select id="getEmpAndDeptByStepTwo" resultType="Dept">
        select * from t_dept where did = #{did}
    </select>
```




----------
###延迟加载
[note type="info flat"]通过使用多表联查，将当前一个完整的过程分布进行，有什么好处？
并不是很麻烦，两个SQL语句放在一起就可以实现一个功能，不放在一起，那么他们各自也可以实现对应的功能。分布查询可以开启延迟加载(懒加载)之后，当前只访问员工信息，只查询员工。如果访问员工以及员工所对应的部门，即会执行当前员工的SQL，又会执行查询部门的SQL。[/note]
MyBatis默认不开启延迟加载，我们需要手动开启

> lazyLoadingEnabled：延迟加载的全局开关。当开启时，所有关联对象都会延迟加载
> aggressiveLazyLoading：当开启时，任何方法的调用都会加载该对象的所有属性。 否则，每个属性会按需加载

我们需要设置**lazyLoadingEnabled**为 [label color="red"]true[/label] ，**aggressiveLazyLoading**为 [label color="default"]false[/label] 。
![6.png][6]

全局配置中开启延迟加载的功能，对于所有分布查询都是会延迟加载。当前有些功能如果不需要延迟加载，就需要通过在分布查询中的一个属性[font size="15.5" color="#240a40"]fetchType[/font]**延迟或立即加载**，使得延迟加载可控。
[font size="15.5" color="#240a40"]fetchType[/font]有两个属性
 - eager立即加载
 - lazy延迟加载

EmpMapper.xml

```xml
    <resultMap id="empAndDeptByStepResultMap" type="Emp">
        <id property="eid" column="eid"></id>
        <result property="empName" column="emp_name"></result>
        <result property="age" column="age"></result>
        <result property="sex" column="sex"></result>
        <result property="email" column="email"></result>
        <!--
            property:处理实体类中多对一的属性
            select:设置分布查询的sql的唯一标识(namespace.SQLId或maapper接口的全类名.方法名)
            column:设置分布查询的条件
            fetchType:当开启全局的延迟加载，可通过此属性手动控制延迟加载的效果
            fetchType = "lazy|eager":lazy表示延迟加载，eager 表示立即加载
        -->
        <association property="dept"
                     select="com.atguigu.mybatis.mapper.DeptMapper.getEmpAndDeptByStepTwo"
                     column="did"
                     fetchType="eager"></association>
    </resultMap>
    <!--Emp getEmpAndDeptByStepOne(@Param("eid") Integer eid);
    第一步：查询员工信息
    -->
    <select id="getEmpAndDeptByStepOne" resultMap="empAndDeptByStepResultMap">
        select * from t_emp where eid = #{eid}
    </select>
```

----------
###一对多的映射处理
一个部门对应多个员工，通过集合来表示部门中所有员工信息

 1. collection标签
DeptMapper接口
```java
    /*
    获取部门以及部门中所有的员工信息
    */
    public abstract Dept getDeptAndEmp(@Param("did") Integer did);
```
DeptMapper.xml
```xml
    <resultMap id="deptAndEmpResultMap" type="Dept">
        <id property="did" column="did"></id>
        <result property="deptName" column="dept_name"></result>
        <!--通过使用collection标签处理一对多的关系
            collection:处理一对多的映射关系
            property:处理一对多关系属性
            ofType:表示该属性所对应的集合中存储数据的类型-->
        <collection property="emps" ofType="Emp">
            <id property="eid" column="eid"></id>
            <result property="empName" column="emp_name"></result>
            <result property="age" column="age"></result>
            <result property="sex" column="sex"></result>
            <result property="email" column="email"></result>
        </collection>
    </resultMap>

    <!--Dept getDeptAndEmp(@Param("did") Integer did);-->
    <select id="getDeptAndEmp" resultMap="deptAndEmpResultMap">
        select * from t_dept left join t_emp on t_dept.did = t_emp.did where t_dept.did = #{did}
    </select>
```

 2. 分步查询

[video title="一对多分步查询 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-22%2015-11-36.mkv " container="b4k5xtx7xcj" subtitle=" " poster=" "] [/video]


DeptMapper.xml
```xml
    <resultMap id="deptAndEmpByStepResultMap" type="Dept">
        <id property="did" column="did"></id>
        <result property="deptName" column="dept_name"></result>
        <!--
        property:处理实体类中多对一的属性
        select:设置分布查询的sql的唯一标识(namespace.SQLId或maapper接口的全类名.方法名)
        column:设置分布查询的条件
        fetchType:当开启全局的延迟加载，可通过此属性手动控制延迟加载的效果
        fetchType = "lazy|eager":lazy表示延迟加载，eager 表示立即加载
        -->
        <collection property="emps"
                    select="com.atguigu.mybatis.mapper.EmpMapper.getDeptAndEmpByStepTwo"
                    column="did" fetchType="eager"></collection>
    </resultMap>
    <!--Dept getDeptAndEmpByStepOne(@Param("did") Integer did);-->
    <!--只需要查询部门信息即可-->
    <select id="getDeptAndEmpByStepOne" resultMap="deptAndEmpByStepResultMap">
        select * from t_dept where did = #{did}
    </select>
```
EmpMapper.xml
```xml
    <!--List<Emp> getDeptAndEmpByStepTwo(@Param("did") Integer did);-->
    <select id="getDeptAndEmpByStepTwo" resultType="Emp">
        select * from t_emp where did = #{did}
    </select>
```


----------
##动态SQL
多条件查询应该什么时候拼接SQL，使用java程序判断实现比较麻烦。mybatis为我们提供了一套动态文件的SQL，方便我们拼接SQL语句。本质就是一系列标签，帮助我们拼接SQL语句
###if标签

 - 根据标签中的test属性所对应的表达式决定标签中的内容是否需要拼接到SQL中
 - 写第一个条件判断之前需要加一个恒成立条件，防止第一个参数为null，语句拼接错误

DynamicSQLMapper.xml
```xml
    <!--List<Emp> getEmpByCondition(Emp emp);-->
    <!-- 1 = 1 的作用:1.可以不影响查询结果2.更好的拼接后面的条件-->
    <select id="getEmpByCondition" resultType="Emp">
        select * from t_emp where 1=1
        <if test="empName != null and empName != ''">
            and emp_name = #{empName}
        </if>
        <if test="age != null and age != ''">
            and age = #{age}
        </if>
        <if test="sex != null and sex != ''">
            and sex = #{sex}
        </if>
        <if test="email != null and email != ''">
            and email = #{email}
        </if>

    </select>
```
![7.png][7]

----------

###where标签
上面的if标签中where标签写死，所以说必须添加**恒成立**条件，还有一种情况就是where后面的条件均不成立，那么where多余了。
如果说我们在上述使用where标签，可以帮助我们**动态生成where关键字**，并且可以将where标签体中的内容前面，多余的and去掉(or)。即使我们将条件均不成立，那么SQL语句将**不会生成where**。
[font size="16" color="#ff0000"]注意：where标签不能将其中内容后面多余的and或or去掉[/font]

```xml
    <select id="getEmpByCondition" resultType="Emp">
        select * from t_emp
        <where>
            <if test="empName != null and empName != ''">
                emp_name = #{empName}
            </if>
            <if test="age != null and age != ''">
                and age = #{age}
            </if>
            <if test="sex != null and sex != ''">
                and sex = #{sex}
            </if>
            <if test="email != null and email != ''">
                and email = #{email}
            </if>
        </where>
    </select>
```
----------
###trim标签
若标签中有内容时：

 1. prefix|suffix:将trim标签中内容前面或后面添加指定内容
 2. prefixOverrides|suffixOverrides:将trim标签中内容前面或后面去掉指定内容
若标签中没有内容时，trim标签也没有任何效果。

DynamicSQLMapper.xml
```xml
    <select id="getEmpByCondition" resultType="Emp">
        select * from t_emp
        <trim prefix="where" suffixOverrides="and|or">
            <if test="empName != null and empName != ''">
                emp_name = #{empName} and
            </if>
            <if test="age != null and age != ''">
                age = #{age} or
            </if>
            <if test="sex != null and sex != ''">
                sex = #{sex} and
            </if>
            <if test="email != null and email != ''">
                email = #{email}
            </if>
        </trim>
    </select>

```


----------
###choose,when,otherwise标签
相当于java中的if...else if...else

 - choose是一个副标签，表示一个完整的if...else if...else结构
 - when和if标签一样
 `<when test=""></when>` 
 - when至少要有一个，otherwise最多只能有一个
DynamicSQLMapper.xml
```xml
    <!--List<Emp> getEmpByChoose(Emp emp);-->
    <select id="getEmpByChoose" resultType="Emp">
        select * from t_emp
        <where>
            <choose>
                <when test="empName != null and empName != ''">
                    emp_name = #{empName}
                </when>
                <when test="age != null and age != ''">
                    age = #{age}
                </when>
                <when test="sex != null and sex != ''">
                    sex = #{sex}
                </when>
                <when test="email != null and email != ''">
                    email = #{email}
                </when>
                <otherwise>
                    did = 1
                </otherwise>
            </choose>
        </where>
    </select>

```

![8.png][8]

----------

###foreach标签
从浏览器中获取到的是一个数组，获取数据id实现批量删除。我们需要循环数组，获取数组中每个数据，然后在 `where id IN (1,2,3)` 就可以实现,或者使用or分隔语句进行删除。
 - 场景：通过数组实现批量删除，通过集合实现批量添加
DynamicSQLMapper接口
```java
    /*
    通过数组实现批量删除
    */

    public abstract int deleteMoreByArray(@Param("eids") Integer[] eids);
```
测试类

```java
    @Test
    public void testDeleteMoreByArray(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        DynamicSQLMapper mapper = sqlSession.getMapper(DynamicSQLMapper.class);
        int result = mapper.deleteMoreByArray(new Integer[]{6, 7, 8, 9, 10, 11});
        System.out.println("result = " + result);
    }
```

 - 使用**IN进行批量删除**
DynamicSQLMapper.xml
```xml
    <!--int deleteMoreByArray(@Param("eids") Integer[] eids);-->
    <delete id="deleteMoreByArray">
        delete from t_emp where eid in
        <!--collection表示我们需要访问到这个数组
        item表示数组中遍历出来的每个元素,表示获取eid就可以
        separator每个遍历来的元素用什么分隔符分隔
        open表示我们当前的所循环的内容以什么开始
        close表示我们当前的所循环的内容以什么结尾
        在SQL语句中IN()可以通过添加open="(" close=")"省略
        -->
        <foreach collection="eids" item="eid" separator="," open="(" close=")">
            #{eid}
        </foreach>
    </delete>

```

 - 使用or连接进行删除
DynamicSQLMapper.xml
```xml
    <!--int deleteMoreByArray(@Param("eids") Integer[] eids);-->
    <delete id="deleteMoreByArray">
        delete from t_emp where
        <foreach collection="eids" item="eid" separator="or">
            eid = #{eid}
        </foreach>
    </delete>
```

 - 场景：通过集合实现批量添加


DynamicSQLMapper接口
```java
    /*
    通过List集合实现批量添加的功能
    */
    public abstract int insertMoreByList(@Param("emps") List<Emp> emps);
```

DynamicSQLMapper.xml
```xml
    <!--int insertMoreByList(@Param("emps") List<Emp> emps);-->
    <insert id="insertMoreByList">
        insert into t_emp values
        <foreach collection="emps" item="emp" separator=",">
            (null,#{emp.empName},#{emp.age},#{emp.sex},#{emp.email},null)
        </foreach>
    </insert>
```

----------
###SQL标签
将我们常用的sql片段进行记录，在我们需要使用的地方，直接 [label color="red"]include[/label] 标签引用该片段。

DynamicSQLMapper.xml
```xml
    <sql id="empColumns">eid,emp_name,age,sex,email</sql>

    <!--List<Emp> getEmpByCondition(Emp emp);-->
    <!-- 1 = 1 的作用:1.可以不影响查询结果2.更好的拼接后面的条件-->
    <select id="getEmpByCondition" resultType="Emp">
        select <include refid="empColumns"></include> from t_emp
        <trim prefix="where" suffixOverrides="and|or">
            <if test="empName != null and empName != ''">
                emp_name = #{empName} and
            </if>
            <if test="age != null and age != ''">
                age = #{age} or
            </if>
            <if test="sex != null and sex != ''">
                sex = #{sex} and
            </if>
            <if test="email != null and email != ''">
                email = #{email}
            </if>
        </trim>
    </select>
```
![9.png][9]

----------
测试类所有源码

```java
public class DynamicSQLMapperTest {
    /*
    动态SQL：
    1.if:根据标签中的test属性所对应的表达式决定标签中的内容是否需要拼接到SQL中
    2.where:当where标签中有内容时，会自动生成where关键字，并且将内容前多余的and或or去掉
    当while标签中没有内容时，此时where标签没有任何效果
    注意：where标签不能将其中内容后面多余的and或or去掉
    3.trim:
    prefix|suffix:将trim标签中内容前面或后面添加指定内容
    prefixOverrides|suffixOverrides:将trim标签中内容前面或后面去掉指定内容

    4.choose,when,otherwise,相当于java中的if...else if...else
    when至少要有一个，otherwise最多只能有一个

    5.foreach标签
    collection：设置需要循环的数组或集合
    item：表示数组或集合中的每一个数据
    separator：循环体之间的分隔符
    open：表示foreach标签所循环的所有内容的开始符号
    close：表示foreach标签所循环的所有内容的结束符号
    6.sql标签
    将我们常用的sql片段进行记录
    设置SQL片段：<sql id="empColumns">eid,emp_name,age,sex,email</sql>
    引用SQL片段：<include refid="empColumns"></include>
     */
    @Test
    public void testInsertMoreByList(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        DynamicSQLMapper mapper = sqlSession.getMapper(DynamicSQLMapper.class);
        Emp emp1 = new Emp(null,"a1",23,"男","123@qq.com",null);
        Emp emp2 = new Emp(null,"a2",23,"男","123@qq.com",null);
        Emp emp3 = new Emp(null,"a3",23,"男","123@qq.com",null);
        List<Emp> emps = Arrays.asList(emp1, emp2, emp3);
        System.out.println(mapper.insertMoreByList(emps));
    }
    @Test
    public void testDeleteMoreByArray(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        DynamicSQLMapper mapper = sqlSession.getMapper(DynamicSQLMapper.class);
        int result = mapper.deleteMoreByArray(new Integer[]{6, 7, 8, 9, 10, 11});
        System.out.println("result = " + result);
    }
    @Test
    public void testGetEmptyByChoose(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        DynamicSQLMapper mapper = sqlSession.getMapper(DynamicSQLMapper.class);
        List<Emp> list = mapper.getEmpByChoose(new Emp(null, "张三", 23,
                "男", "123@qq.com", null));
        System.out.println("list = " + list);
    }

    @Test
    public void testGetEmpByCondition(){
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        DynamicSQLMapper mapper = sqlSession.getMapper(DynamicSQLMapper.class);
        List<Emp> emp = mapper.getEmpByCondition(new Emp(null, "张三", 23,
                "", "", null));
        System.out.println("emp = " + emp);
    }
}
```

----------
##MyBatis的缓存
###一级缓存

缓存就是把我们查询出来的数据进行记录，下次查询相同数据就从缓存中去取，就不会从数据库中访问。
MyBatis会把我们查询的数据进行缓存，再次查询，如果缓存中有，就会从缓存中去取。MyBatis有一级缓存和二级缓存，**一级缓存默认开启**。一级缓存和二级缓存**级别**(范围)不一样，**一级缓存范围是SqlSession级别的**，同一个SqlSession查询出来的数据会被缓存，如果说再通过SqlSession查询相同数据就会从缓存中取。
缓存只对查询功能有效
 - 范围、作用
![10.png][10]
同一个SqlSession中，所查询的数据是会被缓存的，再一次获取缓存中的数据，会从缓存中调用。
![11.png][11]

 - 四种使一级缓存**失效**的情况

 1. 不同的SqlSession**对应不同的一级缓存**，我们没有办法从同一个一级缓存中获取数据
 2. 同一个SqlSession，**但是查询条件不同**，缓存应该是查询过的数据，新数据不会从缓存中取，而是从数据库中访问
 3. 同一个SqlSession，两次查询操作期间**执行了任意一次增删改操作**，缓存会清空。增删改会改变数据库中的数据。缓存方便查询，提高查询效率，但是不能影响查询的结果，如果还从缓存中获取，那么结果将不准确。缓存只是为了提高速度，而不是影响真实性。
![12.png][12]
 4. 同一个SqlSession，两次查询期间**手动清空缓存**
 `sqlSession1.clearCache();//使用此方法手动清空sqlsession的一级缓存` 
 [label color="blue"]clearCache()[/label] 只对一级缓存有效
----------
###二级缓存
二级缓存的范围要比一级缓存的范围要大一点，二级缓存是是**SqlSessionFactory级别**，而且二级缓存需要手动开启。我们通过工厂创建的所有的SqlSession都属于二级缓存范围。
[font size="16" color="7f00ff"]开启条件：[/font]
 1. 在核心配置文件中，设置全局配置属性cacheEnabled="true"，默认为true，不需要设置
 2. 在对应映射文件中设置标签<cache />
 3. 二级缓存必须在SqlSession关闭或提交之后有效，什么叫关闭或提交？
 `sqlSession1.commit();//设置自动提交` 
 `sqlSession1.close();//关闭sqlSession` 
在我们没有关闭或提交SqlSession，查询的数据会被保存到一级缓存中，当我们关闭或者提交SqlSession，数据才会保存到二级缓存中
 4. 查询的数据所转换的实体类类型必须实现序列化的接口
 `public class Emp implements Serializable {}` 
四个条件缺一不可。
![13.png][13]
 - 一种使二级缓存**失效**的情况
 1. 两次查询之间执行了任意的增删改(实际上这个行为一级二级均会被清空)

----------
##MyBatis缓存查询的顺序

[note type="primary flat"]先查询二级缓存，二级缓存中可能会有其他程序已经查询出来的结果，可以直接使用
如果二级缓存没有查到，查询一级缓存
一级缓存没有命中，查询数据库
SqlSession关闭之前，查询出来的数据默认保存在一级缓存中，SqlSession关闭之后，一级缓存中的数据会写入二级缓存。[/note]


----------
##整合第三方缓存EHCache(会配就行)
MyBatis从内存中读取要比磁盘文件中读取要快的很多，但是MyBatis毕竟作为持久层框架，在缓存功能的时候不是很专业，MyBatis提供了一些关于缓存的接口，可以由其他的技术作为MyBatis的二级缓存。只能使用其他第三方技术代替MyBatis的二级缓存，而一级缓存无法替代。

 - pom文件中导入依赖

```xml
<!-- Mybatis EHCache整合包 -->
        <dependency>
            <groupId>org.mybatis.caches</groupId>
            <artifactId>mybatis-ehcache</artifactId>
            <version>1.2.1</version>
        </dependency>
        <!-- slf4j日志门面的一个具体实现 -->
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
        </dependency>
```

 - 创建EHCache的配置文件ehcache.xml（必须这样命名）

```xml
<?xml version="1.0" encoding="utf-8" ?>
<ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="../config/ehcache.xsd">
    <!-- 磁盘保存路径，将ehcache缓存的数据保存到当前磁盘上 -->
    <diskStore path="E:\atguigu\ehcache"/>
    <defaultCache
            maxElementsInMemory="1000"
            maxElementsOnDisk="10000000"
            eternal="false"
            overflowToDisk="true"
            timeToIdleSeconds="120"
            timeToLiveSeconds="120"
            diskExpiryThreadIntervalSeconds="120"
            memoryStoreEvictionPolicy="LRU">
    </defaultCache>
</ehcache>
```

 - 设置二级缓存的类型
CacheMapper.xml
 `<cache type="org.mybatis.caches.ehcache.EhcacheCache" />` 

 - 加入logback日志logback.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration debug="true">
    <!-- 指定日志输出的位置 -->
    <appender name="STDOUT"
              class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
    <!-- 日志输出的格式 -->
    <!-- 按照顺序分别是：时间、日志级别、线程名称、打印日志的类、日志主体内容、换行 -->
    <pattern>[%d{HH:mm:ss.SSS}] [%-5level] [%thread] [%logger] [%msg]%n</pattern>
    </encoder>
    </appender>
    <!-- 设置全局日志级别。日志级别按顺序分别是：DEBUG、INFO、WARN、ERROR -->
    <!-- 指定任何一个日志级别都只打印当前级别和后面级别的日志。 -->
    <root level="DEBUG">
        <!-- 指定打印日志的appender，这里通过“STDOUT”引用了前面配置的appender -->
        <appender-ref ref="STDOUT" />
    </root>
    <!-- 根据特殊需求指定局部日志级别 -->
    <logger name="com.atguigu.crowd.mapper" level="DEBUG"/>
</configuration>
```

----------

##MyBatis的逆向工程(☆)(☆)
本质就是一个代码生成器
正向工程：根据我们创建的java实体类，对应生成数据库表，Hibernate支持，而且帮助我们生成SQL语句。
逆向工程：先创建数据库表，由当前的框架负责根据表生成实体类，mapper接口，映射文件。
###清新简洁版

 1. pom文件中添加依赖和插件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.atguigu.mybatis</groupId>
        <artifactId>MyBatis</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <groupId>com.atguigu.mybatis</groupId>
    <artifactId>MyBatis_MBG</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <!-- 依赖MyBatis核心包 -->
    <dependencies>
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.5.7</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>

        <!-- junit测试 -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
        <!-- MySQL驱动 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.30</version>
        </dependency>

        <!-- log4j日志 -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>

        <!-- https://mvnrepository.com/artifact/com.github.pagehelper/pagehelper -->
        <dependency>
            <groupId>com.github.pagehelper</groupId>
            <artifactId>pagehelper</artifactId>
            <version>5.2.0</version>
        </dependency>

    </dependencies>
    
    <!-- 控制Maven在构建过程中相关配置 -->
    <build>
        <!-- 构建过程中用到的插件 -->
        <plugins>
            <!-- 具体插件，逆向工程的操作是以构建过程中插件形式出现的 -->
            <plugin>
                <groupId>org.mybatis.generator</groupId>
                <artifactId>mybatis-generator-maven-plugin</artifactId>
                <version>1.3.0</version>
                <!-- 插件的依赖 -->
                <dependencies>
                    <!-- 逆向工程的核心依赖 -->
                    <dependency>
                        <groupId>org.mybatis.generator</groupId>
                        <artifactId>mybatis-generator-core</artifactId>
                        <version>1.3.7</version>
                    </dependency>
                    <!-- 数据库连接池 -->
                    <dependency>
                        <groupId>com.mchange</groupId>
                        <artifactId>c3p0</artifactId>
                        <version>0.9.2</version>
                    </dependency>
                    <!-- MySQL驱动 -->
                    <dependency>
                        <groupId>mysql</groupId>
                        <artifactId>mysql-connector-java</artifactId>
                        <version>8.0.30</version>
                    </dependency>


                </dependencies>
            </plugin>
        </plugins>
    </build>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

</project>
```


 2. 创建核心配置文件
包括导入jdbc.properties|log4j.xml|mybatis-config.xml
 3. 创建逆向工程的配置文件
 [label color="red"]文件名必须是generatorConfig.xml[/label] 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE generatorConfiguration
        PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
        "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
<generatorConfiguration>
    <!--
    targetRuntime: 执行生成的逆向工程的版本
        MyBatis3Simple: 生成基本的CRUD（清新简洁版）只有增删改查五个方法
        MyBatis3: 生成带条件的CRUD（奢华尊享版）
    -->
    <context id="DB2Tables" targetRuntime="MyBatis3Simple">
        <!-- 数据库的连接信息 -->
        <jdbcConnection driverClass="com.mysql.cj.jdbc.Driver"
                        connectionURL="jdbc:mysql://localhost:3306/mybatis"
                        userId="root"
                        password="abc123">
            <!--解决mysql8.0以后重复生成所有表的问题-->
            <property name="nullCatalogMeansCurrent" value="true" />
        </jdbcConnection>
        <!-- javaBean的生成策略-->
        <javaModelGenerator targetPackage="com.atguigu.mybatis.pojo" targetProject=".\src\main\java">
            <!--enableSubPackages 是否能够使用子包 . 表示一层路径-->
            <property name="enableSubPackages" value="true" />
            <!--trimStrings 去掉字符串前后空格，解析数据库表反向生成实体类，
            把我们的字段名转换为属性名，字段名前后有空格，可以去除-->
            <property name="trimStrings" value="true" />
        </javaModelGenerator>
        <!-- SQL映射文件的生成策略 -->
        <sqlMapGenerator targetPackage="com.atguigu.mybatis.mapper" targetProject=".\src\main\resources">
            <property name="enableSubPackages" value="true" />
        </sqlMapGenerator>
        <!-- Mapper接口的生成策略 -->
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.atguigu.mybatis.mapper" targetProject=".\src\main\java">
            <property name="enableSubPackages" value="true" />
        </javaClientGenerator>
        <!-- 逆向分析的表 -->
        <!-- tableName设置表名，设置为*号，可以对应所有表，此时不写domainObjectName -->
        <!-- domainObjectName属性指定生成出来的实体类的类名
        mapper接口和映射会根据实体类生成
        -->
        <table tableName="t_emp" domainObjectName="Emp"/>
        <table tableName="t_dept" domainObjectName="Dept"/>
    </context>
</generatorConfiguration>
```

![14.png][14]
就可以自动生成我们需要的东西了，那么当然这种属于 [label color="blue"]清新简洁版[/label] ，只有增删改查五个方法
 [label color="red"]配置文件中对于8+版本的MySQL需要多添加一行信息，防止重复生成所有表问题。[/label] 
 `<property name="nullCatalogMeansCurrent" value="true" />` 


----------
###奢华尊享版(☆)
调整修改targetRuntime `<context id="DB2Tables" targetRuntime="MyBatis3">` 为MyBatis3就可以
对于生成尊享版接口的一点点注解
EmpMapper接口
```java
public interface EmpMapper {

    /*只要看到了方法名带有Example根据条件操作，
    可以以任意字段，任意字段的所有需求作为条件 */
    //根据条件来获取总记录数
    int countByExample(EmpExample example);
    
    //根据条件进行删除
    int deleteByExample(EmpExample example);
    
    //根据主键进行删除
    int deleteByPrimaryKey(Integer eid);
    
    /*普通添加：如果当前传输实体类对象中某个属性的值是null，
    那么我们的普通添加直接会把null作为值赋值给字段，*/
    int insert(Emp record);
    
    /*选择性添加：只会将不是null的属性值为字段赋值，如果有空字段属性值，
    那么就不会出现*/
    int insertSelective(Emp record);
    
    //根据条件查询
    List<Emp> selectByExample(EmpExample example);
    
    //根据主键查询
    Emp selectByPrimaryKey(Integer eid);
    
    //根据条件选择性修改 这里的选择性：如果属性值为null，那么就不会去修改所对应的字段
    int updateByExampleSelective(@Param("record") Emp record, @Param("example") EmpExample example);
    
    //根据条件修改
    int updateByExample(@Param("record") Emp record, @Param("example") EmpExample example);
    
    //根据主键选择性修改
    int updateByPrimaryKeySelective(Emp record);
    
    //根据主键修改
    int updateByPrimaryKey(Emp record);
}

```
不得不说，这样用起来真的巨方便，巨爽，
我使用过程中目前出现了一个问题

```java
public class MBGTest {
    @Test
    public void testMBG(){
        try {
            InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
            SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
            SqlSession sqlSession = sqlSessionFactory.openSession(true);
            EmpMapper mapper = sqlSession.getMapper(EmpMapper.class);

            //查询所有数据
            List<Emp> list = mapper.selectByExample(null);
            list.forEach(emp -> System.out.println(emp));

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}

```

测试类查询所有数据的时候
[note type="warning flat"]org.apache.ibatis.exceptions.PersistenceException:
\### Error querying database.  Cause: java.sql.SQLException: Error setting driver on UnpooledDataSource. Cause: java.lang.ClassNotFoundException: Cannot find class: com.mysql.cj.jdbc.Driver[/note]
我使用8+驱动任何地方都找遍了，我设置了


```xml
        <!-- 只需要在此处添加这一行配置, 重新逆向生成mapper映射文件替换即可 -->
        <plugin type="org.mybatis.generator.plugins.UnmergeableXmlMappersPlugin"/>
```
的配置依然还是会报错，到目前还是没有找到解决办法。
![15.png][15]
后面我在这篇CSDN中找到答案了非常感谢老哥[解决出错][16]，目前我没有找到太好的解决方法，手动导入了一个jar包(唉，都是会用maven的人了怎么又导包)
![16.png][17]
后面查看Maven我大概知道了，主要是因为我把导入的依赖全部放在 [label color="red"]<plugins>标签[/label] 下了，没有真正加载出来，所以说报错了。我调整了导入依赖的文件位置就发现好了

测试类最终源码

```java
public class MBGTest {
    @Test
    public void testMBG(){
        try {
            InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
            SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
            SqlSession sqlSession = sqlSessionFactory.openSession(true);
            EmpMapper mapper = sqlSession.getMapper(EmpMapper.class);

            //查询所有数据
            /*List<Emp> list = mapper.selectByExample(null);
            list.forEach(emp -> System.out.println(emp));*/

            /*根据条件查询 QBC风格，根据条件来查询
            * 条件定义好的，只需要访问相对应的方法
            * 就可以在相对应的SQL语句中生成对应条件
            * */
            //EmpExample example = new EmpExample();

            //创建一个条件,可以使用链式编程添加条件
            //example.createCriteria().andEmpNameEqualTo("张三").andAgeGreaterThanOrEqualTo(20);
            //通过or方法也可以使用or
            /*example.or().andDidIsNotNull();
            List<Emp> list = mapper.selectByExample(example);
            list.forEach(emp -> System.out.println(emp));*/

            //普通修改和选择性修改
            //mapper.updateByPrimaryKey(new Emp(1,"admin",22,null,"456@qq.com",3));
            //mapper.updateByPrimaryKeySelective(new Emp(1,"admin",22,null,"456@qq.com",3));

            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

----------
##分页插件
分页功能可以在MyBatis设置一些相应的功能实现对应的分页，不需要通过书写SQL语句
![17.png][18]
在pom文件中导入依赖

```xml
<!-- https://mvnrepository.com/artifact/com.github.pagehelper/pagehelper -->
<dependency>
<groupId>com.github.pagehelper</groupId>
<artifactId>pagehelper</artifactId>
<version>5.2.0</version>
</dependency>
```
在核心配置文件中添加全局配置，配置插件
mybatis-config.xml

```xml
<plugins>
<!--设置分页插件-->
<plugin interceptor="com.github.pagehelper.PageInterceptor"></plugin>
</plugins>

```

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--引入对应配置文件properties-->
    <properties resource="jdbc.properties"/>
    <!--以包为单位添加类型别名-->
    <typeAliases>
        <package name="com.atguigu.mybatis.pojo"/>
    </typeAliases>

    <plugins>
        <!--设置分页插件-->
        <plugin interceptor="com.github.pagehelper.PageInterceptor"></plugin>
    </plugins>

    <!--连接数据库的环境-->
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>
    </environments>
    <!--以包为单位映入映射文件-->
    <mappers>
        <package name="com.atguigu.mybatis.mapper"/>
    </mappers>
</configuration>
```
测试类测试


我们在页面中设置相关的超链接，我们可以将PageInfo放在域对象中，然后在页面中进行访问。当我们有上一页/下一页我们才需要展示首页和尾页(使用关键字isFirstPage判断)。如果展示导航分页，将navigatepageNums数组进行循环，循环里面写超链接，展示页面，超链接上显示的哪一页就跳转到对应页面。在查询功能之前开启分页，在查询功能之后获取分页相关信息就行。

 [label color="blue"]常用数据：[/label] 
API|功能
:--:|:--:
pageNum|当前页的页码
pageSize|每页显示的条数
size|当前页显示的真实条数
total|总记录数
pages|总页数
prePage|上一页的页码
nextPage|下一页的页码
isFirstPage/isLastPage|是否为第一页/最后一页
hasPreviousPage/hasNextPage|是否存在上一页/下一页
navigatePages|导航分页的页码数
navigatepageNums|导航分页的页码，[1,2,3,4,5]


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/08/3352098195.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/1132286862.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/3701325121.png
  [4]: https://www.kaijavademo.top/29.html#cl-1
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/566810821.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/306024607.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/08/2417583337.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/08/1243673120.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/08/2741984295.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/08/1534607596.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/08/3128976452.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/08/2523936598.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/08/3486966145.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/08/4174856285.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/08/3031447757.png
  [16]: https://blog.csdn.net/note_hsy/article/details/106651870
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/08/3828070019.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/08/33880177.png
  [19]: https://img.kaijavademo.top/typecho/uploads/2023/08/3137201934.jpg