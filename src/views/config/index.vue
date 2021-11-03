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
                        <el-form ref="form" :model="config.USER_ACCOUNTS" label-width="80px">
                            <el-form-item label="二维码验证方式">
                                <el-select v-model="config.USER_ACCOUNTS.type" placeholder="默认为二维码">
                                    <el-option label="二维码" value="qr"></el-option>
                                </el-select>

                            </el-form-item>
                            <el-form-item>
                                <el-input type="query_interval" v-model.number="config.QUERY_INTERVAL"
                                          autocomplete="off"></el-input>
                            </el-form-item>
                                                        <el-form-item>
                                <el-input type="user_heartbeat_interval" v-model.number="config.USER_HEARTBEAT_INTERVAL"
                                          autocomplete="off"></el-input>
                            </el-form-item>

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
            },
            QUERY_INTERVAL: 0.5,
            USER_HEARTBEAT_INTERVAL : 120,
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
