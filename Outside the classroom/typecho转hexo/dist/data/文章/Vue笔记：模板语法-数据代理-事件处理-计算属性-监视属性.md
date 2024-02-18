---
title: Vue笔记：模板语法-数据代理-事件处理-计算属性-监视属性
date: 2023-08-13 08:41:00
categories: Vue
tags: [Vue2,模板语法,前端,数据代理]
---
Vue作为前端主流框架之一，在学习MVC以及以后的路线中需要使用Vue这样的流行的前端技术，需要使用Vue中的一些核心功能和后端进行交互，Vue现在看来必不可少。丰富自己的后端的同时，Vue路线贯穿其中，作此学习笔记。

> Vue官网[Vue][1]

<!--more-->
hello案例
首先我们需要去搭建好一个基本框架，在此之后学习Vue，这一部分始终再html文件中固定。
##基本结构搭建

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>模板语法</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>
<body>
    <!-- 准备好一个容器 -->
    <div id="root">

    </div>
</body>

    <script type="text/javascript" >
        Vue.config.productionTip = false;//阻止vue再启动时产生生产提示。

    </script>

</html>
```
###配置VScode一键生成模板
上面的写法如果在之后的学习中每次书写是比较麻烦，而 [label color="blue"]vscode[/label] 支持自定义生成模板，把我这套模板粘贴到对应的 [label color="orange"]html.json[/label] 中就可以使用了

 - 关于我模板中使用的的书写方法，可以看看这里[el和data的两种写法][2]

![setmodel1.png][3]

```json
	"Vue": {
        "prefix": "!v", // 对应的是使用这个模板的快捷键
        "body": [
        "<!DOCTYPE html>",
        "<html lang=\"zh-CN\">",
        "<head>",
                "\t<meta charset=\"UTF-8\">",
                "\t<title>${1:Title}</title>",  
				"\t<!-- 引入Vue -->",
				"\t<script type=\"text/javascript\" src=\"../js/vue.js\"></script>",		
        "</head>\n",
        "<body>",
				"\t<!--  -->",
				"\t<!-- 准备好一个容器 -->",
                "\t<div id =\"root\">\n\t\t$4\n\t</div>",
        "</body>\n",
        
        "<script type=\"text/javascript\">",
				"\tVue.config.productionTip = false;// 阻止vue再启动时产生生产提示。",
                "\t// 创建Vue实例",
                "\tnew Vue({",
                        "\t\tel: '#root', //vm.$mount('#root')第二种写法，在实例外部可使用",
						"\t\t// 使用函数式的data写法",
                        "\t\tdata(){\n\t\t\treturn{\n\t\t\t\t$2\n\t\t\t}\n\t\t},",
                        "\t\tmethods: {\n\t\t\t$3\n\t\t}",
                "\t});",
        "</script>",
        "</html>"
        ],
        "description": "基于vue的HTML模板" // 模板的描述
        }

```

来看看生成的模板，使用 [label color="red"]!v[/label] 就可以生成模板了(可以自定义快捷键)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!--  -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    // 创建Vue实例
    new Vue({
        el: '#root', //vm.mount('#root')第二种写法，在实例外部可使用
        // 使用函数式的data写法
        data(){
            return{
                
            }
        },
        methods: {
            
        }
    });
</script>
</html>
```

我写的很详细(写了好久QAQ)，添加模板之后，方便之后的学习

----------

需要注意的时 [label color="blue"]vue.js[/label] 被我导入文件夹下，并已经引入。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>初始Vue</title>
    <!-- 引入Vue
    全局多了一个Vue一个内置对象(构造函数)
    -->
    <script type="text/javascript" src="../js/vue.js"></script>
    
</head>
<body>
    <!-- 总结：
    
    初始Vue：
    1.想让Vue工作，就必须创建一个Vue实例，且要传入一个配置对象；
    2.root容器里的代码依然符合html规范，只不过混入了一些特殊的Vue语法；
    3.root容器里的代码被称为【Vue模板】
    模板解析流程：
    先有的流程，然后有的Vue实例，当Vue实例开始工作，发现el里面写了配置，拿取容器
    解析容器，扫描有没有自己设计的特殊语法，然后对于对应数据全部替换，
    生成了一个全新的容器，重新替换刚才的页面

    容器作用：1.为Vue提供模板2.Vue的工作成果的放置位置
    -->

    <!-- 准备好一个容器 -->
    <div id="root">
        <!-- {{}} 分隔符 -->
        <h1>Hello,{{name}}</h1>
    </div>


    <script type="text/javascript" >
        Vue.config.productionTip = false; //阻止 vue 在启动时生成生产提示。

        //创建Vue实例,想用Vue，这里是一切的开端
        
        /*里面需要传递一个配置对象{}
        配置对象：
        axios({
            url:'http://????'
        })
        */
         new Vue({
            //通过id选择器(也可以使用类选择器)找到了对应容器，Vue实例就知道了一会需要把工作成果放在容器中
            el:'#root', //el用于指定当前Vue实例为哪个容器服务，值 通常为css选择器字符串
            data:{
                //data中用于存储数据，数据共el所指定的容器去使用。值我们暂时先写成一个对象，data里面存的是一个对象.
                name:'world'
            }
        })


    </script>
</body>
</html>
```
----------

总结

```html
    <!-- 总结：
    初始Vue：
    1.想让Vue工作，就必须创建一个Vue实例，且要传入一个配置对象；
    2.root容器里的代码依然符合html规范，只不过混入了一些特殊的Vue语法；
    3.root容器里的代码被称为【Vue模板】
    4.Vue实例和容器时一一对应的：
    5.真实开发中只有一个Vue实例，并且会配合着组件一起使用：
    6.{{xxx}}中的xxx要写成js表达式，且xxx可以自动读取到data中的所有属性：
    7.一旦data中的数据发生改变，那么页面中用到该数据的地方也会自动更新:

    注意区分 js表达式 和 js代码(语句)
        1.表达式：一个表达式会产生一个值，可以放在任何一个需要值的地方：
            (1).  a
            (2).  a + b
            (3). demo(1)
            (4). x === y ? 'a' : 'b'
        2.js代码(语句)
            (1) if(){}
            (2) for(){}
            
    -->
```


----------

##模板语法

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>模板语法</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>
<body>
    <!-- Vue模板语法有两大类：
        1.插值语法：
            功能：用于解析标签体内容
            写法：{{xxx}}，xxx是js表达式，且可以读取到data中的所有属性。
        2.指令语法：
            功能：用于解析标签（包括：标签属性、标签体内容、绑定事件.....）
            举例：v-bind:href="xxx" 或简写为 :href="xxx",xxx同样要写js表达式，
                且可以直接读取到data中的所有属性。
            备注：Vue中有很多指令，且形式都是：v-???，此处我们只是拿v-bind举个例子
    -->

    <!-- 准备好一个容器 -->
    <div id="root">
        <h1>插值语法</h1>
        <!-- 插值语法往往用于指定标签体内容  <h1>标签体中</h1>  -->
        <h3>你好，{{name}}</h3>
        <hr>

        <h1>指令语法</h1>
        <!-- 指令语法用于管理标签属性 -->
        <a v-bind:href="school.url.toUpperCase()" x="hello">点我去{{school.name}}学习1</a>
        <!-- 对于想要同时书写两个name属性，可以写多级，相当于创建一个js对象school里面在放一层name -->
        <a :href="school.url" :x="hello">点我去{{school.name}}学习2</a>

    </div>

</body>

<script type="text/javascript">
    Vue.config.productionTip = false;//阻止vue再启动时产生生产提示

    new Vue({
        el:'#root',
        data:{
            name:'jack',
            school:{
                name:'百度',
                url:'http://www.baidu.com',
                hello:'你好'
            }
        }
    })
</script>


</html>
```


----------
##数据绑定
v-bind是一种**单向**的数据绑定，对于数据绑定还有一种双向的数据绑定

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>数据绑定</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>
<body>

    <!-- 
    Vue中有两种数据的绑定方式：
        1.单向绑定(v-bind):数据只能从data流向页面
        2.双向绑定(v-model):数据不仅能从data流向页面，还可以从页面流向data。
          备注：
            1.双向绑定一般都用在表单类元素上(如：input，select等)
            2.v-model:value可以简写为v-model,因为v-model默认收集的就是value值
     -->
    <!--  准备好一个容器 -->
    <div id="root">
        <!-- 普通写法 -->
        <!-- 单向数据绑定：<input type="text" v-bind:value="name"><br>
        双向数据绑定：<input type="text" v-model:value="name"><br> -->

        <!-- 简写 -->
        单向数据绑定：<input type="text" :value="name"><br>
        双向数据绑定：<input type="text" v-model="name"><br>    

        <!-- 如下代码是错误的，因为v-model只能应用在表单类元素(输入类元素)上 
        输入类元素：input,单选框，多选框，select，文本域...
        -->
        <!-- <h2 v-model:x="name">你好啊</h2> -->

    </div>
</body>

    <script type="text/javascript" >
        Vue.config.productionTip = false;//阻止vue再启动时产生生产提示。

        new Vue({
            el:'#root',
            data:{
                name:'尚硅谷'
            }
        })

    </script>

</html>

```
----------
##el和data的两种写法

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>el与data的两种写法</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js" ></script>
</head>
<body>
    <!--  -->
    <!-- 准备好一个容器 -->
    <div id="root">
        <h1>你好，{{name}}</h1>
    </div>
</body>
    <!-- 
        data与el的两种写法
        1.el有2种写法
            (1).new Vue 时候配置el属性
            (2).先创建Vue实例，随后再同通过v.$mount('#root')指定el的值。
        2.data的2种写法
            (1).对象式
            (2).函数式
            如何选择：目前哪种写法都可以，以后学习到组件时，data必须使用函数式，否则会报错。
        3.一个重要的原则：
            由Vue管理的函数(目前就是data)，一定不要写箭头函数，一旦写了箭头函数，this就不再是Vue实例了。
     -->
    
    <script type="text/javascript">
        Vue.config.productionTip = false;

        //el的两种写法
        /* const v = new Vue({
            //el:'#root', //第一种写法
            data:{
                name:'尚硅谷'
            }
        })
        console.log(v)
        v.$mount('#root') */  //第二种写法

        /* 书写一个定时器，让它等待一秒然后执行这句话
         setTimeout(() => {
             v.$mount('#root')
         }, 1000);*/


        //data的两种写法
        new Vue({
            el:'#root',
            //data的第一种写法：对象式
            /*data:{
                name:'尚硅谷'
            }*/

            //data的第二种写法：函数式

            /*学习到组件的时候，必须学习这种麻烦的函数式*/
            /*data:()=>{}
            如果写成箭头函数，this就是全局的window，
            箭头函数没有自己的this，往外找就找到了全局的window
            data:function(){}
            data函数必须老实写成普通函数,在对象里面写方法可以删掉function和 :
            如同:data(){}
            */
            data(){
                console.log('@@@',this) //此处的this是Vue实例对象
                return{
                    name:'尚硅谷'
                }
            }
        })
    </script>

</html>
```

Vue的作者参考了 [label color="blue"]MVVM模型[/label] ，设计了Vue里面的一个特有模型。

> 维基百科[MVVM模型][4]

以后如果使用变量接收Vue实例，使用 [label color="green"]vm[/label] 

```vue
      const vm = new Vue({
          el:'#root',
          data(){
              return {
                  name:'百度',
                  address:'北京'
              }
          }
      })
      console.log(vm)
```
vm上有的东西,原型上有的东西,在今后的模板中都可以使用
![MVVM2.png][5]

```html
    <!-- 
        MVVM模型
            1.M模型(Model)：data中的数据
            2.V视图(View):模板代码
            3.VM:视图模型(ViewModel)：Vue实例
        观察发现：
            1.data中的所有属性，最后都出现在了vm身上。
            2.vm身上的所有属性，及Vue原型上的所有属性，在Vue模板中都可以直接使用。
     -->
```


----------
##Object.defineProperty参数
我们可以通过设置js中的 [label color="blue"]Object.defineProperty[/label] 绑定对象中的一些属性，并设置配置项，也可以将其中的属性和外部属性产生一定的关联

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>回顾Object.defineProperty方法</title>
</head>
<body>
    <script type="text/javascript">
        let number = 18
        let person = {
            name:'张三',
            sex:'男',
            //age:18
        }

        /*Object.defineProperty()
        需要传递三个参数
        参数一：要给哪个对象添加属性？
        参数二：添加的属性名
        参数三：配置项(多个配置项) 
        这样添加出来的属性，是不参与遍历的(枚举)
        

        Object.keys传入对象作为参数
        把传入对象的所有属性名提取出来变成一个数组

        */


        Object.defineProperty(person,'age',{
            //配置基本配置项
            //value:18,
            //enumerable:true,  //控制属性是否可枚举，默认值是false
            //writable:true,   //控制属性是否可以被修改，默认值是false
            //configurable:true //控制属性是否可以被删除，默认值是false
            //配置其他高级项

            //get函数:当有人读取person的age属性时，get函数(getter)就会被调用，且返回值就是age的值

            get:function(){
                console.log('有人读取age属性了')
                return number
            },
            //getter和setter都可以简写
            //set函数:当有人修改person的age属性时，set函数(setter)就会被调用，且会收到修改的具体值
            set(value){
                console.log('有人修改了age属性，且值是',value)
                number = value
            }

        })

        //console.log(Object.keys(person))
        
        // for (let key in person) {
        //     console.log('@',person[key])
        // }
        console.log(person)
    </script>
</body>
</html>
```
##Vue中的数据代理(☆)
**非常非常重要，请多看注解**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Vue中的数据代理</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!-- 
        1.Vue中的数据代理
            通过vm对象来代理data对象中的属性的操作(读/写)
        2.Vue中的数据代理的好处
            更加方便的操作data中的数据
        3.基本理解
            通过Object.defineProperty()把data对象中所有属性添加到vm上
            为每一个添加到vm上的属性，都指定一个getter/setter
            在getter/setter内部在操作(读/写)data中对应的属性。
     -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        <h2>学校名称:{{name}}</h2>
        <h2>学校地址:{{address}}</h2>
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    /*let data = {
        name:'尚硅谷',
        address:'宏福科技园'
    }*/
    // 创建Vue实例
    const vm = new Vue({
        el: '#root',
        /*
        vm._data = options.data = data
        vm._data传入的data
        传入的data 等于 用 options(Vue实例的配置对象).data 表示
        option.data来自于外部定义的data。
        Vue数据代理理解：在Vue实例中，vm对象初始化会有很多属性，其中一个就是_data，
        将data中的数据放入其中。拿到vm之后，添加属性name(通过getter去读取_data)；
        只要有人修改了vm中的属性name，就通过setter映射到_data里面的name进行修改。(Object.defineProperty实现)

        (data作为实参传入，将data的数据保存在_data下，然后又复制一份_data的数据给vm)
        */
        data:{
            name:'尚硅谷',
            address:'宏福科技园'
        }
    });

</script>
</html>
```

----------

##事件处理

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>事件的基本使用</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!-- 
        事件的基本使用：
            1.使用v-on：xxx 或 @xxx 绑定事件，其中xxx是事件名：
            2.事件的回调需要配置在methods对象中，最终会在vm上；
            3.method中配置的函数，不要用箭头函数！否则this就不是vm了：
            4.method中配置的函数，都是被Vue所管理的函数，this指向的是vm 或 组件实例对象；
            5.@Click = "demo" @Click = "demo($event)" 效果一致，但后者可以传参
     -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        <h2>欢迎来到{{name}}学习</h2>
        <!-- 对按钮绑定事件，使用指令
        v-on 当..时候
        当元素被点击(click)的时候,帮我执行一个回调函数showInfo
        -->
        <!-- <button v-on:click="showInfo1">点我提示信息1</button> -->
        <!-- 简写形式： -->
        <button @click="showInfo1">点我提示信息1(不传参)</button>
        <button @click="showInfo2($event,66)">点我提示信息2(传参)</button>
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。

    // 创建Vue实例
    const vm = new Vue({
        el: '#root', //vm.mount('#root')第二种写法，在实例外部可使用
        // 使用函数式的data写法
        data(){
            return{
                name:'尚硅谷'
            }
        },
        methods:{
            // event事件对象，点击按钮，调用函数，默认传递对象event
            showInfo1(event){
            //console.log(event.target.innerText)
            //console.log(this === vm);//此处的this是vm(Vue实例对象)
            alert('同学你好!')
            },

            showInfo2(event,number){
            console.log(event,number)
            //console.log(event.target.innerText)
            //console.log(this === vm);//此处的this是vm(Vue实例对象)
            alert('同学你好!!')
            }
            //showInfo1和showInfo2没有做数据代理，这两个属于固定了，没有必要做数据代理
        }
    });
</script>
</html>
```
----------
##事件修饰符

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
    <style>
        * {
            /* 通过通配符，所有元素之间都有20px的间距 */
            margin-top:20px;
        }
        .demo1 {
            height:50px;
            background-color: skyblue;
        }

        .box1 {
            /* 添加缝隙padding */
            padding: 5px;
            background-color: skyblue;
        }

        
        .box2 {
            /* 添加缝隙padding */
            padding: 5px;
            background-color: orange;
        }

        .list {
            width: 200px;
            height: 200px;
            background-color: peru;
            overflow: auto;
        }

        li {
            height: 100px;

        }
    </style>
</head>

<body>
    <!-- 
        Vue中的事件修饰符：
        1.prevent:阻止默认事件(常用);
        2.stop:阻止事件冒泡(常用);
        3.once:事件只触发一次(常用);

        4.capture:使用事件的捕获模式;
        5.self:只有event，target是当前操作的元素时才是触发事件；
        6.passive：事件的默认行为立即执行，无需等待事件回调执行完毕;
     -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        <h2>欢迎来到{{name}}学习</h2>
        <!-- 阻止默认事件(常用) -->
        <a href="http://www.atguigu.com" @click.prevent="showInfo" >点我提示信息</a>
        <!-- 阻止事件冒泡(常用) -->
        <div class="demo1" @click="showInfo">
            <!-- <button @click.stop="showInfo" >点我提示信息</button> -->
            <!-- 修饰符连续绑定事件，即阻止默认事件又阻止事件冒泡 -->
            <a href="http://www.atguigu.com" @click.prevent.stop="showInfo" >点我提示信息</a>
        </div>
        <!-- 事件只触发一次 -->
        <button @click.once="showInfo" >点我提示信息</button>
        <!-- 使用事件的捕获模式 -->
        <div class="box1" @click.capture="showMsg(1)">
            div1
            <div class="box2" @click="showMsg(2)">
                div2
            </div>
        </div>
        <!-- 只有event，target是当前操作的元素时才是触发事件； -->
        <div class="demo1" @click.self="showInfo">
            <button @click="showInfo" >点我提示信息</button>
        </div>


        <!-- 事件的默认行为立即执行，无需等待事件回调执行完毕; -->
        <ul @scroll="demo" class="list">
            <li>1</li>
            <li>2</li>
            <li>3</li>
            <li>4</li>
        </ul>

    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    // 创建Vue实例
    new Vue({
        el: '#root', //vm.mount('#root')第二种写法，在实例外部可使用
        // 使用函数式的data写法
        data(){
            return{
                name:'尚硅谷'
            }
        },
        methods: {
            showInfo(e){
                //e.stopPropagation()   阻止冒泡
                // preventDefault()     阻止默认行为
                //e.preventDefault() 在Vue中不需要这样书写在@click后面加上.prevent事件修饰符 
                alert('同学你好!')
                //console.log(e.target)
            },
            showMsg(msg){
                console.log(msg)
            },
            demo(){
                //console.log('@')
                for (let i = 0; i < 100000; i++) {
                    console.log('#')
                    
                }
                console.log('累坏了')
            }
        }
    });
</script>
</html>
```

----------
##键盘事件

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!-- 
        1.Vue中常用的按键别名：
            回车 => enter
            删除 => delete (捕获“删除”和“退格”键)
            退出 => esc
            空格 => space
            换行 => tab (特殊，必须配合keydown去使用)
            上 => up
            下 => down
            左 => left
            右 => right

        2.Vue未提供别名的按键，可以使用按键原始的key值去绑定，但注意要转为kebab-case(短横线命名)

        3.系统修饰键(用法特殊)：tab,ctrl,alt,shift,meta
            (1).配合keyup使用：按下修饰键的同时，再按下其他键，随后释放其他键，事件才会被触发
            (2).配合keydown使用：正常触发事件

        4.也可以使用keyCode去指定具体的按键(不推荐)

        5.Vue.config.keyCodes.自定义键名 = 键码, 可以去定制按键别名
     -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        <h2>欢迎来到{{name}}学习</h2>
        <!-- ctrl.y表示按下ctrl + y才可以一起触发事件 -->
        <input type="text" placeholder="按下回车提示输入" @keyup.ctrl.y="showInfo">
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    Vue.config.keyCodes.huiche = 13 //定义了一个别名按键
    // 创建Vue实例
    new Vue({
        el: '#root', //vm.mount('#root')第二种写法，在实例外部可使用
        // 使用函数式的data写法
        data(){
            return{
                name:'尚硅谷'
            }
        },
        methods: {
            showInfo(e){
                //if(e.keyCode !== 13) return   js中可以这样去写判断是否为回车
                console.log(e.target.value);
                //console.log(e.key,e.keyCode);

            }
        }
    });
</script>
</html>
```

----------
##计算属性


```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>姓名案例_计算属性实现</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!-- 
        计算属性：
        1.定义：要用的属性不存在，要通过已有的属性计算得来
        2.原理：底层借助了Object.defineproperty方法提供getter和setter。
        3.get函数什么时候执行？
            (1).初次读取的时候会执行一次
            (2).当依赖数据发生改变的时候会被再次调用
        4.优势：与method实现相比，内部有缓存机制(复用)，效率更高，调试方便。
        5.备注：
            1.计算属性最终会出现在vm上，直接读取使用即可
            2.如果计算属性要被修改，那必须写set函数去响应修改，且set中要引起计算时依赖的数据发生改变。
     -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        姓: <input type="text" v-model="firstName"><br><br>
        名: <input type="text" v-model="lastName"><br><br>
        全名: <span>{{fullName}}</span><br><br>
        <!-- 全名: <span>{{fullName}}</span><br><br>
        全名: <span>{{fullName}}</span><br><br>
        全名: <span>{{fullName}}</span><br><br> -->
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    // 创建Vue实例
    const vm = new Vue({
        el: '#root', //vm.mount('#root')第二种写法，在实例外部可使用
        // 使用函数式的data写法
        data(){
            return{
                firstName:'张',
                lastName:'三' ,
            }
        },
        /*
        对于Vue来说，它会认为data配置项里面所写的就是属性
        所谓的计算属性，就是拿着已经写完的属性去加工，去计算，去生成一个全新的属性
        存放在computed中，需要我们把计算的整个过程配置成对象
        */
        computed:{
            fullName:{
                //get有什么作用？当有人读取fullName时候get就会被调用，且返回值就作为fullName的值
                /*
                get什么时候被调用？
                1.初次读取fullName时。2.所依赖的数据发生变化时。
                */
                //Vue中的get指向调成了vm
                get(){
                    console.log('get被调用了');
                    //console.log(this);    此处的this是vm
                    return this.firstName + '-' + this.lastName
                },
                //set什么时候调用 ? 当fullName被修改的时
                set(value){
                    const arr = value.split('-')
                    this.firstName = arr[0]
                    this.lastName = arr[1]

                }
            }
        }
    });
</script>
</html>

```
如果考虑**只读取不修改**，那么可以使用**简写形式**，但是要注意**插值语法**的写法。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>姓名案例_计算属性实现</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <div id ="root">
        姓: <input type="text" v-model="firstName"><br><br>
        名: <input type="text" v-model="lastName"><br><br>
        全名: <span>{{fullName}}</span><br><br>
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    const vm = new Vue({
        el: '#root', 
        data(){
            return{
                firstName:'张',
                lastName:'三' ,
            }
        },
        computed:{
            //完整写法
            /* fullName:{
                get(){
                    console.log('get被调用了');
                    return this.firstName + '-' + this.lastName
                },
                set(value){
                const arr = value.split('-')
                this.firstName = arr[0]
                this.lastName = arr[1]
                }
            } */

            //简写：前提：set被省略，只读不改
            fullName(){
                //把此函数当成getter函数使用，fullName代表计算属性名
                return this.firstName + '-' + this.lastName
            }
            }
            
        });
</script>
</html>

```

----------
##基于天气案例的监视属性

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>天气案例_监视属性</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!-- 监视属性watch:
    1.当监视属性变化时，回调函数自动调用，进行相关操作
    2.监视的属性必须存在，才能进行监视！！
    3.监视的两种写法：
        (1).new Vue时传入watch配置
        (2).通过vm.$watch监视
    -->
    <!-- 准备好一个容器 -->
    <div id ="root">
        <h2>今天天气很{{info}}</h2>
        <button @click="changeWeather">切换天气</button>
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    // 创建Vue实例
   const vm = new Vue({
       el:'#root',
       data: {
           isHot:true
       },
       computed:{
           info(){
            return this.isHot ? '炎热' : '凉爽'
           }
       },
       methods: {
        changeWeather(){
            this.isHot = !this.isHot
        }
       },
       /*
       Vue实现监视，使用新配置watch,值是配置 属性/计算属性
       里面的key是监视的对象,具体怎么监视，还得写一个配置对象
       handler是一个函数,它可以把对象修改前(oldValue)后(newValue)的值交给我们
       */
       /*watch:{
        isHot:{
            //在这个对象中可以写多个配置....
            immediate:true,//初始化时候让handler把值拿过来调用一下
            //handler什么时候调用？当isHot发生改变时。
            handler(newValue,oldValue){
                console.log('isHot被修改了',newValue,oldValue)
            }
        }
       }*/
      
    })
        //可以不通过watch配置，通过vm也可以实现一个监视,保证实例已经创建完了
        /*通过vm.$watch() 参数一：要监视的对象(带单引号)
        参数二：要书写具体监视的内容，写成一个配置对象
        
        */
        vm.$watch('isHot',{
            //在这个对象中可以写多个配置....
            immediate:true,//初始化时候让handler把值拿过来调用一下
            //handler什么时候调用？当isHot发生改变时。
            handler(newValue,oldValue){
                console.log('isHot被修改了',newValue,oldValue)
            }
        })

</script>
</html>
```
###深度监视

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>天气案例_深度监视</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <!-- 深度监视：
            (1).Vue中的watch默认不监测对象内部值的改变(一层)
            (2).配置deep:true可以监测对象内部值改变(多层)
        备注：
            (1).Vue自身可以检测对象内部值的改变，但Vue提供的watch默认不可以！
            (2).使用watch时根据数据的具体结构，决定是否采用深度监视。
    -->
    <div id ="root">
        <h2>今天天气很{{info}}</h2>
        <button @click="changeWeather">切换天气</button>
        <hr>
        <h3>a的值是:{{numbers.a}}</h3>
        <button @click="numbers.a++">点我让a + 1</button>
        <h3>b的值是:{{numbers.b}}</h3>
        <button @click="numbers.b++">点我让b + 1</button>
        <button @click="numbers = {a:666,b:888}" >彻底替换掉numbers</button>
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    // 创建Vue实例
   const vm = new Vue({
       el:'#root',
       data: {
           isHot:true,
           numbers:{
               a:1,
               b:1
           }
       },
       computed:{
           info(){
            return this.isHot ? '炎热' : '凉爽'
           }
       },
       methods: {
        changeWeather(){
            this.isHot = !this.isHot
        }
       },
       watch:{
        isHot:{
            //在这个对象中可以写多个配置....
            //immediate:true,//初始化时候让handler把值拿过来调用一下
            //handler什么时候调用？当isHot发生改变时。
            handler(newValue,oldValue){
                console.log('isHot被修改了',newValue,oldValue)
            }
        },
        //监视多级结构中，某个属性的变化
        /*
        'numbers.a':{
            handler(){
                console.log('a被改变了');
            }
        }*/
        numbers:{
            //开启深度监视
            //监视多级结构中，所有属性的变化
            deep:true,
            handler(){
                console.log('numbers改变了');
            }
        }
       }
      
    })

</script>
</html>
```

###监视的简写形式

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>天气案例_监视属性_简写</title>
    <!-- 引入Vue -->
    <script type="text/javascript" src="../js/vue.js"></script>
</head>

<body>
    <div id ="root">
        <h2>今天天气很{{info}}</h2>
        <button @click="changeWeather">切换天气</button>
    </div>
</body>

<script type="text/javascript">
    Vue.config.productionTip = false;// 阻止vue再启动时产生生产提示。
    // 创建Vue实例
   const vm = new Vue({
       el:'#root',
       data: {
           isHot:true
       },
       computed:{
           info(){
            return this.isHot ? '炎热' : '凉爽'
           }
       },
       methods: {
        changeWeather(){
            this.isHot = !this.isHot
        }
       },
       watch:{
           //正常第一种写法
           /* isHot:{
            //immediate:true,//初始化时候让handler把值拿过来调用一下
            //deep:true,  //深度监视
            handler(newValue,oldValue){
                console.log('isHot被修改了',newValue,oldValue)
            }
        },*/

        //简写
        //简写形式的前提：配置项中只有handler就可以开启简写形式
        /*
        isHot(newValue,oldValue){
            console.log('isHot被修改了',newValue,oldValue)
        }
        */
       }
      
    })

    //正常第二种写法
    /*vm.$watch('isHot',{
            immediate:true,//初始化时候让handler把值拿过来调用一下
            deep:true,  //深度监视
            handler(newValue,oldValue){
                console.log('isHot被修改了',newValue,oldValue)
            }
        })*/
    //简写,无法配置immediate:true；deep:true
    vm.$watch('isHot',function(newValue,oldValue){
        console.log('isHot被修改了',newValue,oldValue)
    })


    //简写不允许写成箭头函数，会造成指向问题，所有vue所管理的函数，都要写成普通函数
</script>
</html>
```







  [1]: https://cn.vuejs.org/
  [2]: https://www.kaijavademo.top/323.html#cl-5
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/1976815754.png
  [4]: https://zh.wikipedia.org/wiki/MVVM
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/4140168645.png