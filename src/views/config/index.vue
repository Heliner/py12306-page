<template>
    <div id="account-index" class="container">
        <el-container>
            <el-row :gutter="40" class="width-full">
                <el-col class="data">
                    <div v-loading="loading_lists">
                        <el-form ref="form" :model="config" label-width="280px">
                            <el-form-item label="二维码验证方式">
                                <el-select v-model="config.USER_ACCOUNTS[0].type" placeholder="默认为二维码">
                                    <el-option label="二维码" value="qr"/>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="乘客">
                                <el-input type="text" v-model="config.QUERY_JOBS[0].members"
                                          placeholder="与已认证乘客一致,如:张三,李四">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="查询间隔(秒)">
                                <el-tooltip class="item" effect="dark" content="请勿低于5秒否则可能会造成ip被封" placement="top">
                                    <el-input type="number" v-model="config.QUERY_INTERVAL"
                                              autocomplete="off">
                                    </el-input>
                                </el-tooltip>
                            </el-form-item>
                            <el-form-item label="出发站点">
                                <el-input type="text" v-model="config.QUERY_JOBS[0].stations.left"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="到达站点">
                                <el-input type="text" v-model="config.QUERY_JOBS[0].stations.arrive"
                                          autocomplete="off">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="出发日期">
                                <el-input type="text" v-model="config.QUERY_JOBS[0].left_dates"
                                          autocomplete="off" placeholder="如2021-10-1,1998-2-2">
                                </el-input>
                            </el-form-item>
                            <el-form-item label="座位类型">
                                <el-select v-model="config.QUERY_JOBS[0].seats" multiple
                                           placeholder="请选择">
                                    <el-option
                                        v-for="item in seats_options"
                                        :key="item"
                                        :label="item"
                                        :value="item">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="车次">
                                <el-input type="text" v-model="config.QUERY_JOBS[0].train_numbers"
                                          autocomplete="off" placeholder="如K10,G632;为空代表全选">
                                </el-input>
                            </el-form-item>
                            <div class="text-align" style="text-align: center">
                                <el-button type="primary" @click="setConfig()">提交</el-button>
                            </div>
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
                    [{
                        'key': 0, // 如使用多个账号 key 不能重复
                        'user_name': 'your user name',
                        'password': '忽略',
                        'type': 'qr',
                        // qr 为扫码登录，填写其他为密码登录
                    },],
                QUERY_INTERVAL: 0.5,
                USER_HEARTBEAT_INTERVAL: 120,
                QUERY_JOBS: [
                    {
                        account_key: 0,
                        stations: {
                            left: '',
                            arrive: '',

                        },
                        left_dates: '',
                        seats: [],
                        train_numbers: '',
                        members: '',
                    }
                ],

            },
            tmp: {
                inputVisible: true,
                inputValue: '',
            },
            seats_options: [
                '特等座', '商务座', '一等座', '二等座', '软卧', '硬卧', '动卧', '软座', '硬座', '无座'
            ],
            retry_time:
                5,
            auto_refresh:
                true
        }
    },
    mounted() {
        this.getConfig()
    },
    methods: {
        async getConfig() {
            await this.$api.get_config().then(res => {
                console.log(res)
                if (res.data) {
                    this.config = this.parseBackEnd2Front(res.data)
                } else {
                    console.warn("not get config data from backend")
                }
            }).catch(error => {
                console.log("not handled error :" + error)
            })
        },
        async setConfig() {
            await this.$api.set_config(this.parseFront2Backend(this.config)).then(res => {
            }).catch(error => {
                console.log("not handled error :" + error)
            })
        },
        parseFront2Backend: function (config_data) {
            // 复制原来的config到新的变量中，并将原来的类list的字符串转化为list
            let backendConfig = JSON.parse(JSON.stringify(config_data));
            console.log(backendConfig)
            for (let idx in backendConfig.USER_ACCOUNTS) {
            }
            //对于某些属性需要进行类型转化
            backendConfig.QUERY_INTERVAL = Number.parseInt(backendConfig.QUERY_INTERVAL)
            for (let idx in backendConfig.QUERY_JOBS) {
                let query_job = backendConfig.QUERY_JOBS[idx]
                console.log(query_job)
                query_job.members = this.parseStr2List(query_job.members)
                query_job.left_dates = this.parseStr2List(query_job.left_dates)
                query_job.train_numbers = this.parseStr2List(query_job.train_numbers)

                for (let station_idx in query_job.stations) {
                    // 转化left_dates, train_numbers, members字段
                }
            }
            return backendConfig
        },
        parseBackEnd2Front: function (config_data) {
            let frontConfig = JSON.parse(JSON.stringify(config_data));
            for (let idx in frontConfig.USER_ACCOUNTS) {
            }
            for (let idx in frontConfig.QUERY_JOBS) {
                let query_job = frontConfig.QUERY_JOBS[idx]
                query_job.members = this.parseList2Str(query_job.members)
                query_job.left_dates = this.parseList2Str(query_job.left_dates)
                query_job.train_numbers = this.parseList2Str(query_job.train_numbers)

                for (let station_idx in query_job.stations) {
                    // 转化left_dates, train_numbers, members字段
                }
            }
            return frontConfig
        },
        parseStr2List: function (list_str) {
            let splited_list = list_str.split(',')
            let res_list = []
            for (let idx in splited_list) {
                let splited_str = splited_list[idx]
                if ('' === splited_str) {
                    continue
                }
                res_list.push(splited_str)
            }
            console.log(list_str)
            console.log(res_list)
            return res_list
        },
        parseList2Str: function (list) {
            return list.join(",")
        }

    }
}
</script>

<style scoped lang="scss">
@import "../../assets/scss/variables";

</style>
