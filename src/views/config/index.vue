<template>
    <div id="account-index" class="container">
        <el-container>
            <el-row class="width-full">
                <el-col class="data">
                    <div class="card padding-tb-1-rem padding-lr-2-rem" v-loading="loading_lists">
                        <el-form ref="form" :model="config" label-width="280px">
                            <el-form-item label="二维码验证方式">
                                <el-select v-model="config.USER_ACCOUNTS_TF[0].type" placeholder="默认为二维码">
                                    <el-option label="二维码" value="qr"/>
                                </el-select>
                            </el-form-item>
                           <el-form-item label="乘客">
                                <el-input type="text" v-model="config.QUERY_JOBS_TF[0].members" placeholder="与已认证乘客一致,如:张三,李四">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="查询间隔(秒)">
                                <el-input type="number" v-model="config.QUERY_INTERVAL"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="登录状态检查间隔(秒)">
                                <el-input type="number" v-model="config.USER_HEARTBEAT_INTERVAL"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <!--                            事件标签-->
                            <el-form-item label="出发站点">
                                <el-input type="text" v-model="config.QUERY_JOBS_TF[0].stations[0].left"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="到达站点">
                                <el-input type="text" v-model="config.QUERY_JOBS_TF[0].stations[0].arrive"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="出发日期">
                                <el-input type="text" v-model="config.QUERY_JOBS_TF[0].stations[0].left_dates"
                                          autocomplete="off" placeholder="如2021-10-1,1998-2-2">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="座位类型">
                                <el-select v-model="config.QUERY_JOBS_TF[0].stations[0].seats" multiple placeholder="请选择">
                                    <el-option
                                      v-for="item in seats_options"
                                      :key="item"
                                      :label="item"
                                      :value="item">
                                    </el-option>
                                  </el-select>
                            </el-form-item>
                            <el-form-item label="车次">
                                <el-input type="text" v-model="config.QUERY_JOBS_TF[0].stations[0].train_numbers"
                                          autocomplete="off" placeholder="如K10,G632;为空代表全选">
                                </el-input>
                            </el-form-item>
                        </el-form>
                    </div>
                </el-col>
            </el-row>
        </el-container>
    </div>
</template>

<script>

import config from "../../plugins/axios/config";

export default {
    data() {
        return {
            empty: false,
            config: {
                // 需要替換的項目使用_TF結尾
                USER_ACCOUNTS:
                    [{
                        'key': 0, // 如使用多个账号 key 不能重复
                        'user_name': 'your user name',
                        'password': '忽略',
                        'type': 'qr',
                        // qr 为扫码登录，填写其他为密码登录
                    },],
                USER_ACCOUNTS_TF: [{
                    'key': 0, // 如使用多个账号 key 不能重复
                    'user_name': 'your user name',
                    'password': '忽略',
                    'type': 'qr',
                    // qr 为扫码登录，填写其他为密码登录
                },],
                QUERY_INTERVAL: 0.5,
                USER_HEARTBEAT_INTERVAL: 120,
                QUERY_JOBS: [],
                QUERY_JOBS_TF: [
                    {
                        account_key: 0,
                        stations: [{
                            left: '',
                            arrive: '',
                            left_dates:'',
                            seats:[],
                            train_numbers:'',
                        }]
                    }
                ],

            },
            tmp:{
                inputVisible:true,
                inputValue:'',
            },
            seats_options:[
                '特等座', '商务座', '一等座', '二等座', '软卧', '硬卧', '动卧', '软座', '硬座', '无座'
            ],
            loading_lists: false,
            retry_time:
                5,
            auto_refresh:
                true
        }
    },
    mounted() {
        this.refreshData()
    },
    methods: {
        async refreshData() {
            if (this.$route.path != '/config') return
            if (this.auto_refresh)
                await this.getLists()
            setTimeout(this.refreshData, this.retry_time * 1000)
        },
        async getLists(loading = true) {
            if (loading) this.loading_lists = true
            await this.$api.get_query().then(res => {
                if (!res.data || res.data.length <= 0) this.empty = true
                else this.empty = false
                this.lists = res.data
                this.loading_lists = false
            }).catch(error => {
                this.loading_lists = false
            })
        },
        parseFront2Backend:function (){
            // 复制原来的config到新的变量中，并将原来的类list的字符串转化为list
            let backendData = {}

        },
    }
}
</script>

<style scoped lang="scss">
@import "../../assets/scss/variables";

</style>
