<template>
  <div class="home">
    <el-container>
      <el-header>
        <el-page-header @back="goBack" content="首页">
        </el-page-header>
      </el-header>
      <el-main>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
          <el-form-item label="地区">
            <el-select v-model="formInline.city" placeholder="请选择所查询的地区">
              <el-option label="温州市本级" value="温州市"></el-option>
              <el-option label="鹿城区" value="鹿城区"></el-option>
              <el-option label="龙湾区" value="龙湾区"></el-option>
              <el-option label="瓯海区" value="瓯海区"></el-option>
              <el-option label="温州开发区" value="温州开发区"></el-option>
              <el-option label="瓯江口" value="瓯江口"></el-option>
              <el-option label="洞头区" value="洞头区"></el-option>
              <el-option label="永嘉县" value="永嘉县"></el-option>
              <el-option label="平阳县" value="平阳县"></el-option>
              <el-option label="苍南县" value="苍南县"></el-option>
              <el-option label="泰顺县" value="泰顺县"></el-option>
              <el-option label="文成县" value="文成县"></el-option>
              <el-option label="瑞安市" value="瑞安市"></el-option>
              <el-option label="乐清市" value="乐清市"></el-option>
              <el-option label="龙港市" value="龙港市"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="项目名称">
            <el-input v-model="formInline.content" placeholder="请输入项目名称" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">查询</el-button>
          </el-form-item>
        </el-form>
          <el-table :data="AllData.alldata" fit='true' style="width: 100%" height="510" :header-cell-style="{textAlign: 'center'}" :cell-style="{ textAlign: 'center' }">
            <el-table-column prop="district_name" label="地区" width="350" sortable>
            </el-table-column>
            <el-table-column prop="title" label="标题" width="750" sortable>
              <template slot-scope="scope">
                <el-link :href="'/content/'+scope.row.noteid" target="_blank">{{scope.row.title}}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="日期" width="350" sortable>
            </el-table-column>
          </el-table>
          
          <!-- <el-col :span="4"><div class="grid-content bg-purple"></div></el-col> -->
        </el-row>
        
      </el-main>
      <el-footer>测试中</el-footer>
    </el-container>
  </div>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";
import {GetAll} from "../apis/read";
import { reactive,ref,onMounted} from "@vue/composition-api"
import dateFormat from "../utils/date"
import { GetInfoPost } from "../apis/read";

export default {
  name: "Home",
  components: {
    HelloWorld,
  },
  setup(props,context){
      const AllData = reactive({
        alldata:[]
      });
      GetAll().then(res =>{
        AllData.alldata = res.data.data;
        for (let item of AllData.alldata){
          item.date = dateFormat(item.date)
        }
      });

      onMounted(()=>{
        
      })

      return {
        AllData,
        dateFormat,
      }
    },
  data() {
    return {
        formInline: {
          city:'',
          content:''
        }
      }
    },
    methods: {
      onSubmit() {
        const postparams = reactive ({
          url:'/',
          key:[
          this.city=this.formInline.city,
          this.content=this.formInline.content]
          
        })
      GetInfoPost(postparams).then(res =>{
            this.AllData.alldata = res.data.data;
            for (let item of this.AllData.alldata){
              item.date = dateFormat(item.date)
            }
        })
      },
      goBack() {
        location.reload();
      }
    }
};
</script>
<style scoped lang="scss">

</style>