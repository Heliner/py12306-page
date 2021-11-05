<template>
    <div id="account-index" class="container">
        <el-container>
            <el-row class="width-full">
                <div class="action-group">
                    <h2 class="action-title">查询任务</h2>
                    <div class="refresh-switch">
                        <span class="helper-text margin-right-s5-rem">自动刷新 <span v-text="retry_time"></span> 秒</span>
                        <el-switch v-model="auto_refresh"></el-switch>
                    </div>
                </div>

                <el-col class="data" v-else>
                    <div class="card padding-tb-1-rem padding-lr-2-rem" v-loading="loading_lists">
                        <el-form ref="form" :model="config" label-width="80px">
                            <el-form-item>
                                <el-input type="number" v-model="config.USER_ACCOUNTS_TF[0].KEY"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input type="number" v-model="config.USER_ACCOUNTS_TF[0].USER_NAME"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input type="number" v-model="config.USER_ACCOUNTS_TF[0].PASSWORD"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="二维码验证方式">
                                <el-select v-model="config.USER_ACCOUNTS_TF[0].TYPE" placeholder="默认为二维码">
                                    <el-option label="二维码" value="qr"/>
                                </el-select>
                            </el-form-item>
                            <el-form-item>
                                <el-input type="number" v-model="config.QUERY_INTERVAL"
                                          autocomplete="off">

                                </el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input type="number" v-model="config.USER_HEARTBEAT_INTERVAL"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input type="number" v-model="config.QUERY_JOB_THREAD_ENABLED"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <!--                            路程設定 -->
                            <el-table :data="config.QUERY_JOBS" style="width: 100%" border>
                                <el-table-column type="selection" width="55" align="center">
                                </el-table-column>
                                <el-table-column align="center">
                                    <template slot="header" slot-scope="scope">
                                        <span style="color:#2d65dc;">成员名称</span>
                                        <i style="color:#F56C6C;">*</i>
                                    </template>
                                    <template slot-scope="scope">
                                        <el-form-item
                                            :prop="'QUERY_JOBS.' + scope.$index + '.account_key'">
                                            <el-input
                                                type="text"
                                                autocomplete="off"
                                            ></el-input>
                                        </el-form-item>
                                    </template>
                                </el-table-column>
                                <el-table-column align="center">
                                    <template slot="header" slot-scope="scope">
                                        <span style="color:#2d65dc;">成员值</span>
                                        <i style="color:#F56C6C;">*</i>
                                    </template>
                                    <template slot-scope="scope">
                                        <el-form-item
                                            :prop="'params.' + scope.$index + '.value'"
                                            :rules="addJsonForm.addJsonRules.value"
                                        >
                                            <el-input
                                                type="text"
                                                v-model="scope.row.value"
                                                autocomplete="off"
                                            ></el-input>
                                        </el-form-item>
                                    </template>
                                </el-table-column>
                            </el-table>
                            <!--                        變更后需要處理重啓的重要配置         -->
                        </el-form>

                    </div>
                </el-col>
            </el-row>
        </el-container>
    </div>
</template>

<script>

export default {
    data() {
        return {
            empty: false,
            config: {
                // 需要替換的項目使用_TF結尾
                USER_ACCOUNTS:
                    {
                        'key': 0, // 如使用多个账号 key 不能重复
                        'user_name':
                            'your user name',
                        'password':
                            '忽略',
                        'type':
                            'qr'
                        // qr 为扫码登录，填写其他为密码登录
                    },
                USER_ACCOUNTS_TF: {
                    key:0,
                    user_name:'',
                    password:'',
                    type:'qr',
                },
                QUERY_INTERVAL: 0.5,
                USER_HEARTBEAT_INTERVAL: 120,
                QUERY_JOBS: [],
                QUERY_JOBS_TF:[],
            },

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
        }
    }
}
</script>

<style scoped lang="scss">
@import "../../assets/scss/variables";

</style>
