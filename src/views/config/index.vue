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
                            <!--                            事件标签-->
                            <el-form-item label="账户key" hidden="true">
                                <el-input type="number" v-model="config.QUERY_JOBS_TF[0].account_key"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="出发站点">
                                <el-input type="number" v-model="config.QUERY_JOBS_TF[0].stations.left"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>

                            <el-form-item label="到达站点">
                                <el-input type="number" v-model="config.QUERY_JOBS_TF[0].stations.arrive"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="到达站点">
                                <el-input type="number" v-model="config.QUERY_JOBS_TF[0].stations.arrive"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-tag
                                    :key="tag"
                                    v-for="tag in dynamicTags"
                                    closable
                                    :disable-transitions="false"
                                    @close="handleClose(tag)">
                                    {{ tag }}
                                </el-tag>
                                <el-input
                                    class="input-new-tag"
                                    v-if="inputVisible"
                                    v-model="inputValue"
                                    ref="saveTagInput"
                                    size="small"
                                    @keyup.enter.native="handleInputConfirm"
                                    @blur="handleInputConfirm"
                                >
                                </el-input>
                                <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 日期
                                </el-button>
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
                    {
                        'key': 0, // 如使用多个账号 key 不能重复
                        'user_name': 'your user name',
                        'password': '忽略',
                        'type': 'qr',
                        // qr 为扫码登录，填写其他为密码登录
                    },
                USER_ACCOUNTS_TF: {
                    ...config.USER_ACCOUNTS
                },
                QUERY_INTERVAL: 0.5,
                USER_HEARTBEAT_INTERVAL: 120,
                QUERY_JOBS: [],
                QUERY_JOBS_TF: [...config.QUERY_JOBS],
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
        },
        handleClose(tag) {
            this.config.QUERY_JOBS_TF.left_dates.splice(this.config.QUERY_JOBS_TF.left_dates.indexOf(tag), 1);
        },

        showInput() {
            this.inputVisible = true;
            this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },

        handleInputConfirm() {
            let inputValue = this.inputValue;
            if (inputValue) {
                this.dynamicTags.push(inputValue);
            }
            this.inputVisible = false;
            this.inputValue = '';
        }
    }
}
</script>

<style scoped lang="scss">
@import "../../assets/scss/variables";

</style>
