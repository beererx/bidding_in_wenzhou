<template>
  <el-container>
    <el-header>
      <el-page-header @back="goBack" content="正文">
      </el-page-header>
    </el-header>
    <el-main>
      <el-row>
        <el-col align="center" :span="16" :offset="4" style=" background: #f7fbfc">
          <p align="left" v-html="items.detailsitems[0].information">This is some text in a very short paragraph</p>
          <el-link :href="items.detailsitems[0].link"><el-button type="primary">查看原文</el-button></el-link>
        </el-col>
      </el-row>
    </el-main>
    <el-footer>测试中</el-footer>
  </el-container>
</template>

<script>
import { reactive,ref,onMounted} from "@vue/composition-api"
import { GetInfoPost } from "../apis/read";

export default {
  name: "Content",
  components: {
  },
  setup(props,context){
      const items = reactive({
            detailsitems:[]
      })

      const detailparams= reactive({
        url:context.root.$route.path,
        key:""
      })

      GetInfoPost(detailparams).then(res =>{
        console.log('dwefwrefb',res)
          items.detailsitems = res.data.data
      })


      onMounted(()=>{
        
      })

      return {
        items
      }
    },
  data() {
    return {

      }
    },
    methods: {
      goBack() {
        window.close();
      }
    }
};
</script>

<style scoped lang="scss">

</style>