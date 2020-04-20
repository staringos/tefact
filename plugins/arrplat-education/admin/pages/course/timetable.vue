<template>
  <!--<ArrPanel title="课程表" border>-->
    <!--<el-calendar v-model="value">-->
    <!--</el-calendar>-->
    <!---->
  <!--</ArrPanel>-->
  <div class="main-container edu">
    <div class="panel panel-bordered false">
      <div class="header">
        <el-row :gutter="20">
          <el-col :span="2">
            <div>课程表</div>
          </el-col>
          <el-col :span="5" class="user_select_con">
            <div class="user_select_title" style="width: 60px">校区：</div>
            <el-select
              @change="campusChange"
              class="user_select_item"
              v-model="campusSelect"
              placeholder="请选择">
              <el-option
                v-for="(item,index) in campus"
                :key="index"
                :label="item.campus_name"
                :value="item.campus_id">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="6" class="user_select_con">
            <div class="user_select_title">上课老师：</div>
            <el-select
              @change="employeeSChange"
              v-model="employeeSelect"
              multiple
              collapse-tags
              placeholder="全部">
              <el-option
                v-for="(item,index) in employee"
                :key="index"
                :label="item.nickname"
                :value="item.id">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="7" class="user_select_con">
            <div class="user_select_title">乐器类型：</div>
            <el-select
              clearable
              @change="instrumentChange"
              v-model="instrumentSelect"
              multiple
              collapse-tags
              placeholder="全部">
              <el-option
                v-for="(item,index) in instrument"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-date-picker
              v-model="eduTime"
              @change="getEduTime"
              type="date"
              placeholder="选择日期"
              format="yyyy-MM-dd"
              value-format="timestamp"
              style="width: 100%">
            </el-date-picker>
          </el-col>
        </el-row>
      </div>
      <div class="table">
        <el-table
          v-loading="loading"
          :data="tableData"
          :span-method="objectSpanMethod"
          @cell-click="getCreateTime"
          style="width: 100%"
          border
          max-height="630">
          <el-table-column
            fixed
            fixed="left"
            prop="date"
            label="日期"
            width="150">
            <template slot-scope="scope">
              <p>{{scope.row.day_date}}</p>
              <p>{{scope.row.day_name}}</p>
            </template>
          </el-table-column>
          <el-table-column
            fixed="left"
            label="老师"
            prop="teacher_name"
            width="120">
            <template slot-scope="scope">
              <div v-if="scope.row.values.teacher_name">{{scope.row.values.teacher_name}}({{scope.row.values.reserve_num+'/'+scope.row.values.course_num}})</div>
            </template>
          </el-table-column>
          <el-table-column
            label="8:00-9:00"
            prop="course_type"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[0].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[0].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[0].course_color}" @click="handleZsk(scope.row.values.list[0])">
                    <div v-if="scope.row.values.list[0].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[0].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[0].level_name}}</p>
                    <p class="center">{{scope.row.values.list[0].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[0].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[0].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[0].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[0])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[0].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[0].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[0])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[0].course_type : 0) == 0 || !scope.row.values.list[0].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="9:00-10:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[1].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[1].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[1].course_color}" @click="handleZsk(scope.row.values.list[1])">
                    <div v-if="scope.row.values.list[1].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[1].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[1].level_name}}</p>
                    <p class="center">{{scope.row.values.list[1].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[1].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[1].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[1].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[1])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[1].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[1].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[1])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[1].course_type : 0) == 0 || !scope.row.values.list[1].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="10:00-11:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[2].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[2].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[2].course_color}" @click="handleZsk(scope.row.values.list[2])">
                    <div v-if="scope.row.values.list[2].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[2].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[2].level_name}}</p>
                    <p class="center">{{scope.row.values.list[2].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[2].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[2].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[2].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[2])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[2].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[2].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[2])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[2].course_type : 0) == 0 || !scope.row.values.list[2].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="11:00-12:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[3].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[3].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[3].course_color}" @click="handleZsk(scope.row.values.list[3])">
                    <div v-if="scope.row.values.list[3].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[3].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[3].level_name}}</p>
                    <p class="center">{{scope.row.values.list[3].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[3].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[3].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[3].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[3])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[3].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[3].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[3])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[3].course_type : 0) == 0 || !scope.row.values.list[3].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="13:00-14:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[4].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[4].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[4].course_color}" @click="handleZsk(scope.row.values.list[4])">
                    <div v-if="scope.row.values.list[4].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[4].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[4].level_name}}</p>
                    <p class="center">{{scope.row.values.list[4].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[4].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[4].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[4].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[4])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[4].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[4].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[4])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[4].course_type : 0) == 0 || !scope.row.values.list[4].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="14:00-15:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[5].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[5].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[5].course_color}" @click="handleZsk(scope.row.values.list[5])">
                    <div v-if="scope.row.values.list[5].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[5].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[5].level_name}}</p>
                    <p class="center">{{scope.row.values.list[5].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[5].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[5].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[5].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[5])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[5].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[5].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[5])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[5].course_type : 0) == 0 || !scope.row.values.list[5].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="15:00-16:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[6].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[6].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[6].course_color}" @click="handleZsk(scope.row.values.list[6])">
                    <div v-if="scope.row.values.list[6].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[6].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[6].level_name}}</p>
                    <p class="center">{{scope.row.values.list[6].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[6].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[6].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[6].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[6])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[6].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[6].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[6])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[6].course_type : 0) == 0 || !scope.row.values.list[6].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="16:00-17:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[7].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[7].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[7].course_color}" @click="handleZsk(scope.row.values.list[7])">
                    <div v-if="scope.row.values.list[7].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[7].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[7].level_name}}</p>
                    <p class="center">{{scope.row.values.list[7].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[7].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[7].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[7].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[7])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[7].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[7].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[7])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[7].course_type : 0) == 0 || !scope.row.values.list[7].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="17:00-18:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[8].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[8].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[8].course_color}" @click="handleZsk(scope.row.values.list[8])">
                    <div v-if="scope.row.values.list[8].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[8].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[8].level_name}}</p>
                    <p class="center">{{scope.row.values.list[8].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[8].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[8].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[8].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[8])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[8].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[8].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[8])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[8].course_type : 0) == 0 || !scope.row.values.list[8].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="18:00-19:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[9].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[9].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[9].course_color}" @click="handleZsk(scope.row.values.list[9])">
                    <div v-if="scope.row.values.list[9].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[9].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[9].level_name}}</p>
                    <p class="center">{{scope.row.values.list[9].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[9].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[9].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[9].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[9])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[9].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[9].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[9])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[9].course_type : 0) == 0 || !scope.row.values.list[9].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="19:00-20:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[10].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[10].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[10].course_color}" @click="handleZsk(scope.row.values.list[10])">
                    <div v-if="scope.row.values.list[10].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[10].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[10].level_name}}</p>
                    <p class="center">{{scope.row.values.list[10].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[10].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[10].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[10].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[10])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[10].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[10].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[10])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[10].course_type : 0) == 0 || !scope.row.values.list[10].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="20:00-21:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[11].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[11].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[11].course_color}" @click="handleZsk(scope.row.values.list[11])">
                    <div v-if="scope.row.values.list[11].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[11].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[11].level_name}}</p>
                    <p class="center">{{scope.row.values.list[11].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[11].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[11].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[11].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[11])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[11].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[11].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[11])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[11].course_type : 0) == 0 || !scope.row.values.list[11].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="time"
            label="21:00-22:00"
            width="120">
            <template slot-scope="scope">
              <div v-if="(scope.row.values.list? scope.row.values.list[12].course_type : 0) == 1">
                <el-tooltip :content="scope.row.values.list[12].remark" placement="top">
                  <div class="zsk" :style="{'background': scope.row.values.list[12].course_color}" @click="handleZsk(scope.row.values.list[12])">
                    <div v-if="scope.row.values.list[12].subscript" class= "triangle">
                      <input type= "text" v-model="scope.row.values.list[12].subscript" class = "text"/>
                    </div>
                    <p class="top">{{scope.row.values.list[12].level_name}}</p>
                    <p class="center">{{scope.row.values.list[12].class_room_name}}</p>
                    <p class="bottom">{{scope.row.values.list[12].course_name}}</p>
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[12].course_type : 0) == 2">
                <el-tooltip :content="scope.row.values.list[12].remark" placement="top">
                  <div class="stk" @click="handleStk(scope.row.values.list[12])">
                    试听课
                  </div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[12].course_type : 0) == 3">
                <el-tooltip :content="scope.row.values.list[12].remark" placement="top">
                  <div class="yzy" @click="handleZy(scope.row.values.list[12])">已占用</div>
                </el-tooltip>
              </div>
              <div v-if="(scope.row.values.list? scope.row.values.list[12].course_type : 0) == 0 || !scope.row.values.list[12].course_type">
                <div @click="handlePop(scope.row)" class="el-icon-plus"></div>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <!-- 课程类型 -->
      <el-dialog
        title="课程类型"
        :visible.sync="dialogVisible"
        width="30%"
        :before-close="handleClose">
        <el-button type="primary" @click="alertFormalCourse">正式课</el-button>
        <el-button type="success" @click="alertAuditionCourse">试听课</el-button>
        <el-button type="danger" @click="alertOccupy">占  用</el-button>
      </el-dialog>
      <!-- 移除正式课问询弹窗 -->
      <el-dialog
        title="确定移除课程吗？"
        :visible.sync="dialogDeleteZsk"
        width="40%"
        :before-close="deleteZskClose">
        <el-form class="alert_add_stk alert_delete_zsk" ref="addStk" :model="addStk" label-width="80px">
          <el-form-item label-width="100px" label="批量移除课程">
            <el-radio-group v-model="deleteCourseControl">
              <el-radio label="1">不使用</el-radio>
              <el-radio label="2">使用批量移除</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item v-if="deleteCourseControl == 2" label-width="100px" label="设置日期周期">
            <el-date-picker
              v-model="deleteZskDate"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item v-if="deleteCourseControl == 2" label-width="100px" label="设置周几上课">
            <el-checkbox-group class="week" v-model="deleteWeekDay">
              <el-checkbox label="1">周一</el-checkbox>
              <el-checkbox label="2">周二</el-checkbox>
              <el-checkbox label="3">周三</el-checkbox>
              <el-checkbox label="4">周四</el-checkbox>
              <el-checkbox label="5">周五</el-checkbox>
              <el-checkbox label="6">周六</el-checkbox>
              <el-checkbox label="7">周日</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="deleteZskClose">取 消</el-button>
            <el-button type="primary" @click="deleteZskTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 正式课移除确认弹窗 -->
      <el-dialog
        title="确定移除课程吗？"
        :visible.sync="deleteZskStudent"
        width="40%"
        :before-close="handleZskClose">
        <span>有以下学生报名：</span>
        <el-tag
          v-for="tag in studentSignList"
          :key="tag.student_name"
          :type="tag.student_id">
          {{tag.student_name}}
        </el-tag>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleZskClose">取 消</el-button>
            <el-button type="primary" @click="handleZskTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 移除试听课课问询弹窗 -->
      <el-dialog
        title="确定移除课程吗？"
        :visible.sync="dialogDeleteStk"
        width="40%"
        :before-close="handleZyClose">
        <span>你现在正要将试听课移除？</span>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleZyClose">取 消</el-button>
            <el-button type="primary" @click="handleZyTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 添加编辑试听课弹窗 -->
      <el-dialog
        title="添加试听课"
        :visible.sync="dialogAddStk"
        width="40%"
        :before-close="handleStkClose">
        <el-form class="alert_add_stk" ref="addStk" :model="addStk" label-width="80px">
          <el-form-item class="must-fill" label="选择客户">
            <el-autocomplete
              style="width: 80%"
              class="inline-input"
              v-model="customer"
              :fetch-suggestions="selectCustomer"
              placeholder="请输入内容"
              @select="handleSelectBusiness"
            ></el-autocomplete>
            <span @click="createCustomer" style="color: blue;cursor: pointer">新建客户</span>
          </el-form-item>
          <el-form-item class="must-fill" label="选择商机">
            <el-select
              @change="businessChange"
              v-model="business"
              placeholder="请选择商机">
              <el-option
                v-for="(item,index) in selectBusiness"
                :key="index"
                :label="item.business_name"
                :value="item.business_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="must-fill" label="试听时间">
            <el-input class="ty_input_class" v-model="clickTime"></el-input>
          </el-form-item>
          <el-form-item class="must-fill" label="上课老师">
            <el-input class="ty_input_class" :disabled="true" v-model="teacherSelect"></el-input>
          </el-form-item>
          <el-form-item class="must-fill" label="上课校区">
            <el-input class="ty_input_class" :disabled="true" v-model="campusSelect"></el-input>
          </el-form-item>
          <el-form-item label="上课教室">
            <el-select
              @change="classRoomChange"
              v-model="classRoomFirst"
              placeholder="去选择上课的教室">
              <el-option
                v-for="(item,index) in classRoom"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="must-fill" label="销售人员">
            <el-select
              @change="peopleListChange"
              v-model="getPeople"
              placeholder="去选择销售人员">
              <el-option
                v-for="(item,index) in getPeopleList"
                :key="index"
                :label="item.nickname"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="getStkDesc"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleStkClose">取 消</el-button>
            <el-button type="primary" @click="handleStkTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 添加编辑正式课弹窗 -->
      <el-dialog
        title="添加正式课"
        :visible.sync="dialogAddZsk"
        width="40%"
        :before-close="handleZshClose">
        <el-form class="alert_add_zsk" ref="addZsk" :model="addZsk" label-width="80px">
          <el-form-item label-width="auto" label="仅自己学员可见">
            <el-switch v-model="isStudent"></el-switch>
          </el-form-item>
          <el-form-item class="must-fill" label-width="100px" label="课程种类">
            <el-select
              @change="changeBaseCourse"
              v-model="selectBaseCourse"
              placeholder="请选择课程种类">
              <el-option
                v-for="(item,index) in baseCourselist"
                :key="index"
                :label="item.course_type_name"
                :value="item.course_type_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="must-fill" label-width="100px" label="课程名">
            <el-select
              v-model="courseTitle"
              @change="changeCourseTitle"
              placeholder="请选择课程名称">
              <el-option
                v-for="(item,index) in courseTitleList"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="must-fill" label-width="100px" label="上课校区">
            <el-input class="ty_input_class" v-model="campusSelect"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="上课教室">
            <el-select
              @change="classRoomChange"
              v-model="classRoomFirst"
              placeholder="请选择上课教室">
              <el-option
                v-for="(item,index) in classRoom"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label-width="100px" label="上课学员">
            <el-select
              v-model="zskStudent"
              multiple
              filterable
              remote
              reserve-keyword
              placeholder="请输入关键词"
              @change="changeZskStudent"
              :remote-method="getStudent">
              <el-option
                v-for="item in studentList"
                :key="item.id"
                :label="item.name"
                :value="item.name">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="must-fill" label-width="100px" label="课程等级">
            <el-select
              clearable
              @change="changeCourseLevel"
              v-model="classLevel"
              placeholder="课程等级">
              <el-option
                v-for="(item,index) in courseLevelList"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="must-fill" label-width="100px" label="选择素材">
            <el-select
              @change="changeMaterial"
              v-model="materialSelect"
              multiple
              collapse-tags
              placeholder="全部">
              <el-option
                v-for="(item,index) in materialList"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label-width="100px" label="老师看备注">
            <el-input type="textarea" v-model="zskRemark"></el-input>
          </el-form-item>
          <el-form-item v-if="edit" label-width="100px" label="批量建课周期">
            <el-radio-group v-model="createCourse">
              <el-radio label="1">不使用批量</el-radio>
              <el-radio label="2">使用批量建课</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item v-if="createCourse == 2" label-width="100px" label="设置日期周期">
            <el-date-picker
              v-model="setZskDate"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item v-if="createCourse == 2" label-width="100px" label="设置周几上课">
            <el-checkbox-group class="week" v-model="zskWeekDay">
              <el-checkbox label="1">周一</el-checkbox>
              <el-checkbox label="2">周二</el-checkbox>
              <el-checkbox label="3">周三</el-checkbox>
              <el-checkbox label="4">周四</el-checkbox>
              <el-checkbox label="5">周五</el-checkbox>
              <el-checkbox label="6">周六</el-checkbox>
              <el-checkbox label="7">周日</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label-width="100px" label="是否添加标签">
            <el-radio-group v-model="createLabel">
              <el-radio label="1">不添加</el-radio>
              <el-radio label="2">添加</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item v-if="createLabel == 2" label-width="100px" label="角标内容">
            <el-input
              v-model="zskSubscript"
              type="text"
              placeholder="请输入内容"
              maxlength="4"
              show-word-limit
            ></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleZshClose">取 消</el-button>
            <el-button type="primary" @click="handleZshTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 编辑问询正式课弹窗 -->
      <el-dialog
        title="正式课"
        :visible.sync="dialogShowZsk"
        width="40%"
        :before-close="handleShowStkClose">
        <el-table
          :data="studentSignList"
          style="width:100%"
          height="250"
          class="handleShowStkClose">
          <el-table-column
            fixed
            label="姓名"
            width="150">
            <template slot-scope="scope">
              <span style="color: blue">{{scope.row.student_name}}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="签到"
            width="100">
            <template slot-scope="scope">
              <span style="color: green" @click="zskSignIn(scope.row)">已签到</span>
            </template>
          </el-table-column>
          <el-table-column
            label="预约"
            width="150">
            <template slot-scope="scope">
              <span style="color: red" @click="zskCancel(scope.row)">取消预约</span>
            </template>
          </el-table-column>
          <el-table-column
            label="旷课">
            <template slot-scope="scope">
              <span  style="color: #FF8400" @click="zskTruancy(scope.row)">学生旷课</span>
            </template>
          </el-table-column>
        </el-table>
        <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="alertEditAuditionClass">编 辑</el-button>
            <el-button type="danger" @click="handleShowZskTrue">移 除</el-button>
            <el-button @click="handleShowStkClose">取 消</el-button>
          </span>
      </el-dialog>
      <!-- 编辑问询试听课弹窗 -->
      <el-dialog
        title="试听课"
        :visible.sync="dialogShowStk"
        width="40%"
        :before-close="handleShowStkClose">
        <el-table
          :data="studentSignList"
          style="width:100%"
          height="250"
          class="handleShowStkClose">
          <el-table-column
            fixed
            label="姓名"
            width="150">
            <template slot-scope="scope">
              <span style="color: blue">{{scope.row.student_name}}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="qiandao"
            label="签到"
            width="100">
            <template slot-scope="scope">
              <span style="color: green" @click="stkSignIn(scope.row)">已签到</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="daodian"
            label="到店"
            width="150">
            <template slot-scope="scope">
              <span style="color: red" @click="stkShop(scope.row)">无意向到店</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="shuangyue"
            label="爽约">
            <template slot-scope="scope">
              <span style="color: #FF8400" @click="stkSy(scope.row)">爽约</span>
            </template>
          </el-table-column>
        </el-table>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="alertEditAuditionCourse">编 辑</el-button>
          <el-button type="danger" @click="handleShowStkTrue">移 除</el-button>
          <el-button @click="handleShowStkClose">取 消</el-button>
        </span>
      </el-dialog>
      <!-- 试听课到店 爽约 正式课取消预约 学生旷课 -->
      <el-dialog
        title=""
        :visible.sync="dialogStkShop"
        width="40%"
        :before-close="handleStkShopClose">
        <div slot="title">
          <span class="title-age">确认把{{studentRowData.student_name}}的课程取消吗？</span>
        </div>
        <el-form v-if="dialogStkShop" class="alert_add_zsk" :model="stkReason" :rules="infoRules" ref="stkReason" label-width="80px">
          <el-form-item prop="desc" label-width="100px" label="填写原因">
            <el-input type="textarea" v-model="stkReason.desc"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleStkShopClose">取 消</el-button>
            <el-button type="primary" @click="handleStkShopTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 试听课签到 -->
      <el-dialog
        title="试听课签到"
        :visible.sync="dialogStkSign"
        width="40%"
        :before-close="handleStkSignClose">
        <el-form class="alert_add_zsk" ref="addZsk" :model="addCustomer" label-width="80px">
          <el-form-item label-width="100px" label="客户意向">
            <el-radio-group class="week" v-model="customerIntention">
              <el-radio :label="1">考虑中</el-radio>
              <el-radio :label="2">已成单</el-radio>
              <el-radio :label="3">确认不购</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label-width="100px" label="填写原因">
            <el-input type="textarea" v-model="stkShopReason"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button v-if="customerIntention == 2" type="success">新建订单</el-button>
            <el-button @click="handleStkSignClose">取 消</el-button>
            <el-button type="primary" @click="handleStkSignTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 正式课体系课签到 -->
      <el-dialog
        title="签到"
        :visible.sync="dialogZskSign"
        width="40%"
        class="signZsk"
        :before-close="handleZskSignClose">
        <!-- 历史签到记录 -->
        <el-form class="alert_add_zsk" ref="addZsk" :model="historySignInList" label-width="80px">
          <p class="zsk_sign_title">为{{this.studentRowData.student_name}}学员{{this.historySignTime}}：</p>
          <el-form-item label-width="100px" label="选择主题">
            <el-select
              v-model="historyListArr"
              multiple
              disabled
              collapse-tags
              placeholder="选择主题（多选）">
              <el-option
                v-for="item in historyList"
                :key="item.subject_id"
                :label="item.subject_name"
                :value="item.subject_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-collapse class="zsk_sign_content" v-model="selectThemeHistoryList">
            <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
              <div slot="title">
                <div>
                  <span>{{item.subject_name}}</span>
                  <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                </div>
              </div>
              <div v-for="(list,n) in item.values">
                <div class="second_content">
                  <span class="second_content_title">{{list.essential_name}}</span>
                  <template>
                    <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                      <el-radio disabled :label= '1'>未开始</el-radio>
                      <el-radio disabled :label= '2'>进行中</el-radio>
                      <el-radio disabled :label= '3'>已结束</el-radio>
                    </el-radio-group>
                  </template>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
          <el-form-item label-width="100px" label="回课备注1">
            <el-input :disabled="true" type="textarea" v-model="historySignInList.teacher_remark"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="回课备注2">
            <el-input :disabled="true" type="textarea" v-model="historySignInList.student_remark"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="选择素材">
            <el-select
              v-model="materialSelect"
              multiple
              disabled
              collapse-tags
              placeholder="全部">
              <el-option
                v-for="(item,index) in materialList"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label-width="100px" label="学员等级">
            <el-select
              clearable
              disabled
              v-model="historySignInList.level_name"
              placeholder="上课学员是多选">
              <el-option
                v-for="item in getStudentLevelList"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <!-- 签到记录 -->
        <el-form class="alert_add_zsk" ref="addZsk" :model="addCustomer" label-width="80px">
          <p class="zsk_sign_title">为{{this.studentRowData.student_name}}学员{{this.getSignInTime}}的课程进行签到：</p>
          <el-form-item label-width="100px" label="选择主题">
            <el-select
              v-model="historyListArr"
              multiple
              collapse-tags
              @change="changeTheme"
              placeholder="选择主题（多选）">
              <el-option
                v-for="item in historyList"
                :key="item.subject_id"
                :label="item.subject_name"
                :value="item.subject_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-collapse class="zsk_sign_content" v-model="selectThemeList">
            <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
              <div slot="title">
                <div>
                  <span>{{item.subject_name}}</span>
                  <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                  <span @click.stop.prevent="deleteContentList(item.subject_id)" style="color: red">删除</span>
                </div>
              </div>
              <div v-for="(list,n) in item.values">
                <div class="second_content">
                  <span class="second_content_title">{{list.essential_name}}</span>
                  <template>
                    <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                      <el-radio :label= '1'>未开始</el-radio>
                      <el-radio :label= '2'>进行中</el-radio>
                      <el-radio :label= '3'>已结束</el-radio>
                    </el-radio-group>
                  </template>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
          <el-form-item label-width="100px" label="回课备注1">
            <el-input type="textarea" v-model="teacherRemark"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="回课备注2">
            <el-input type="textarea" v-model="studentRemark"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="选择素材">
            <el-select
              @change="changeSelectMaterial"
              v-model="materialSelect"
              multiple
              collapse-tags
              placeholder="全部">
              <el-option
                v-for="(item,index) in materialList"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label-width="100px" label="学员等级">
            <el-select
              clearable
              @change="changeStudentLevel"
              v-model="selectStudentLevel"
              placeholder="请选择学员等级">
              <el-option
                v-for="item in getStudentLevelList"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleZskSignClose">取 消</el-button>
            <el-button type="primary" @click="handleZskSignTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 正式课非体系课签到 -->
      <el-dialog
        title="签到"
        :visible.sync="dialogZskNoSystem"
        width="40%"
        class="signZsk"
        :before-close="handleZskSignClose">
        <el-form class="alert_add_zsk" ref="addZsk" :model="addCustomer" label-width="80px">
          <p class="zsk_sign_title">为{{this.studentRowData.student_name}}学员{{this.getSignInTime}}的课程进行签到：</p>
          <el-form-item label-width="100px" label="选择主题">
            <el-select
              v-model="historyListArr"
              multiple
              collapse-tags
              @change="changeTheme"
              placeholder="选择主题（多选）">
              <el-option
                v-for="item in historyList"
                :key="item.subject_id"
                :label="item.subject_name"
                :value="item.subject_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-collapse class="zsk_sign_content" v-model="selectThemeList">
            <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
              <div slot="title">
                <div>
                  <span>{{item.subject_name}}</span>
                  <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                  <span @click.stop.prevent="deleteContentList(item.subject_id)" style="color: red">删除</span>
                </div>
              </div>
              <div v-for="(list,n) in item.values">
                <div class="second_content">
                  <span class="second_content_title">{{list.essential_name}}</span>
                  <template>
                    <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                      <el-radio :label= '1'>未开始</el-radio>
                      <el-radio :label= '2'>进行中</el-radio>
                      <el-radio :label= '3'>已结束</el-radio>
                    </el-radio-group>
                  </template>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
          <el-form-item label-width="100px" label="课程素材">
            <el-select
              @change="changeSelectMaterial"
              v-model="materialSelect"
              multiple
              collapse-tags
              placeholder="全部">
              <el-option
                v-for="(item,index) in materialList"
                :key="index"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label-width="100px" label="回课备注1">
            <el-input type="textarea" v-model="teacherRemark"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="回课备注2">
            <el-input type="textarea" v-model="studentRemark"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleZskSignClose">取 消</el-button>
            <el-button type="primary" @click="handleZskSignTrue">确 定</el-button>
          </span>
      </el-dialog>
      <!-- 添加占用弹窗 -->
      <course-occupy @occupy-close="addOccupy" :dialogAddZy="dialogAddZy"></course-occupy>
      <!-- 移除占用弹窗 -->
      <delete-occupy @delete-occupy="deleteOccupy" :dialogDeleteZy="dialogDeleteZy"></delete-occupy>
      <!-- 新建客户弹窗 -->
      <EntityModifier entityKey="edu_customer" @onChanged="handleCustomerSaved"></EntityModifier>

      <!--<course-audition :dialogAddStkDatas="dialogAddStkData"></course-audition>-->
    </div>
  </div>
</template>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import { infoRules } from '../../components/formRules'
  import EntityModifier from '~/components/entities/EntityModifier.vue'
  import CourseOccupy from '../../components/global/CourseOccupy'
  import DeleteOccupy from '../../components/global/DeleteOccupy'
  import CourseAudition from "../../components/global/CourseAudition"
  const edu = namespace('education')
  const app = namespace('app')
  const entities = namespace('entities')

  @Component({
    layout: 'plugin',
    components: {CourseAudition,  EntityModifier, CourseOccupy, DeleteOccupy }
  })
  export default class UIndex extends Vue {
    value = new Date()
    @edu.Action getCampus
    @edu.Action getCourse
    @edu.Action curriculum
    @edu.Action getCustomer
    @edu.Action baseCourse
    @edu.Action courseLevel
    @edu.Action material
    @edu.Action student
    @edu.Action courseSign
    @edu.Action deleteCourse
    @edu.Action getEditAudition
    @edu.Action campusClassroom
    @edu.Action getClassSign
    @edu.Action studentLevel
    @edu.Action getCourseSignLists
    @edu.Action getInstrumentType
    @app.Getter currentOrgIdGetter
    @entities.Action toggleModifyDialog
    @edu.Action userHistory



    async getFirstCampus(){
      const res = await this.getCampus({types: 'info', org_id: this.org_id})
      if(res.status == 200){
        let campus_id = res.data.data.campus_id
        if(this.userHistoryObj.campus_id){
          campus_id = this.userHistoryObj.campus_id
        }
        this.getSchool(campus_id);
      }
    }
    async getSchool(campus_id){
      const res = await this.getCampus({types: 'campus', org_id: this.org_id})
      if(res.status == 200 && res.data.data.list){
        this.campus = res.data.data.list
        if(this.campus.length > 0){
          for(var i=0;i<this.campus.length;i++){
            if(this.campus[i].campus_id == campus_id){
              this.campusSelect = this.campus[i].campus_name
              this.employee = this.campus[i].values
              this.campusId = this.campus[i].campus_id
              if(this.userHistoryObj.teacher_employee_id){
                if(this.userHistoryObj.teacher_employee_id.includes(',')){
                  this.employeeSelect = this.userHistoryObj.teacher_employee_id.split(',')
                }else{
                  this.employeeSelect.push(this.userHistoryObj.teacher_employee_id)
                }
              }
            }
          }
        }
        this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)
        console.log('res:', res)
      }
    }
    async getInstrument(){
      const instrument = await this.getInstrumentType({org_id: this.org_id})
      if(instrument.status == 200 && instrument.data.data.list && instrument.data.data.list.length>0){
        this.instrument = instrument.data.data.list
        if(this.userHistoryObj.instrument_type_id){
          if(this.userHistoryObj.instrument_type_id.includes(',')){
            this.instrumentSelect = this.userHistoryObj.instrument_type_id.split(',')
          }else{
            this.instrumentSelect.push(this.userHistoryObj.instrument_type_id)
          }
        }
      }
    }
    async getList(campusId, teacherEmployeeId, instrumentTypeId, startTime){
      if(!startTime){
        startTime = 0
      }else{
        startTime = startTime/1000
      }
      const course = await this.getCourse({org_id: this.org_id ,campusId: campusId, teacherEmployeeId: teacherEmployeeId,instrumentTypeId: instrumentTypeId, startTime: startTime})
      this.tableData = course.data.data.list
      this.gethebingArr()
      this.loading = false
      console.log('list:',course)
    }
    async getBaseCourse(){
      const res = await this.baseCourse({org_id: this.org_id,campus_id :this.campusId})
      if(res.status == 200){
        this.baseCourselist = res.data.data.list
      }
    }
    async getUserHistory(){
      const res = await this.userHistory()
      if(res.status == 200){
        this.userHistoryObj = res.data.data
        this.teacherEmployeeId = this.userHistoryObj.teacher_employee_id
        this.instrumentTypeId = this.userHistoryObj.instrument_type_id
        this.getInstrument()
        this.getFirstCampus()
      }
    }
    async mounted() {
      this.getUserHistory()
      this.org_id = this.currentOrgIdGetter
    }

    // 添加占用 试听课 正式课方法
    async addCurriculum(data){
      data.teacher_employee_id = this.teacherId
      data.org_id = this.org_id
      const res = await this.curriculum( data )
      if(res.status == 200){
        this.$message({message: '添加成功', type: 'success'})
        this.handleClose()
        this.handleZshClose()
        this.handleStkClose()
        this.defaultStk()
        this.defaultZsk()
        this.handleShowStkClose()
        this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)
      }else{
        this.$message.error('添加失败');
      }
    }
    // 添加试听课默认参数
    defaultStk(){
      this.edit = true
      this.isDelete = false
      this.getStkDesc = ''
      this.classRoomFirst = ''
      this.classroomId = ''
      this.getPeople = ''
      this.sale_employee_id = ''
      this.customer = ''
      this.customerId = ''
      this.business = ''
      this.businessId = ''
    }
    // 添加正式课默认参数
    defaultZsk(){
      this.edit = true
      this.isStudent = true
      this.isDelete = false
      this.createLabel = '1'
      this.selectBaseCourse = ''
      this.courseTitle = ''
      this.courseTitleId = ''
      this.classRoomFirst = ''
      this.classroomId = ''
      this.zskStudent = []
      this.zskRemark = ''
      this.classLevelId = ''
      this.classLevel = ''
      this.materialSelectId = ''
      this.zskSubscript = ''
      this.dialogAddZsk = false
      this.materialSelect = []
      this.createCourse = '1'
      this.zskWeekDay = []
      this.setZskDate = []

    }
    // 监听校区
    campusChange(val){
      this.loading = true
      this.employee = []
      this.employeeSelect = []
      this.getEmployee(val)
      this.campusId = val
      let obj:any = {};
      obj = this.campus.find((item)=>{
        return item.campus_id === val
      })
      this.campusSelect = obj.campus_name
      this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)
    }
    // 获取老师
    getEmployee(id){
      for(var i = 0;i < this.campus.length; i++){
        if(this.campus[i].campus_id == id){
          this.employee = this.campus[i].values
        }
      }
    }
    // 监听时间筛选
    getEduTime(val){
      this.eduTime = val
      this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)
    }
    // 监听雇员
    employeeSChange(val){
      this.loading = true
      let str: string = '';
      if(val.length == 1){
        str = val[0]
        // 获取雇员昵称
        let obj:any = {};
        obj = this.employee.find((item)=>{
          return item.id === val[0];
        });
      }else{
        str = val.toString()
      }
      this.teacherEmployeeId = str;
      this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)

    }
    // 监听乐器类型
    instrumentChange(val){
      this.loading = true
      this.instrumentTypeId = val;
      this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)
    }
    // 表格合并方法-提供数组
    gethebingArr(){
      let obj: any = {}
      let arr:any = []
      this.rowArr = []
      this.tableData.forEach(function(item){
        obj[item.day_time] ? (obj[item.day_time].count += 1) : obj[item.day_time] = {count: 1}
      })
      for(let i in obj){
        arr.push(obj[i].count)
      }
      for(let i=0;i<arr.length;i++){
        if(arr[i]){
          this.rowArr.push(arr[i])
          for(var j=0;j<arr[i]-1;j++){
            this.rowArr.push(0)
          }
        }else{
          this.rowArr.push(0)
        }
      }
    }
    // 表格合并方法
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 0) {
        const item = this.rowArr[rowIndex];
        return {
          rowspan: item,
          colspan: 1
        };
      }
    }
    // 创建课程时间戳
    getCreateTime(row,column,event,cell){
      let timeStr: string = column.label
      this.teacherSelect = row.values.teacher_name
      this.teacherId = row.values.id
      let newTime = row.day_date.replace(/-/,'年').replace('-','月')+'日'
      this.getSignInTime =  newTime +' '+ timeStr
      this.startHour = timeStr.split('-')[0].split(':')[0]
      let time: string = row.day_date
      this.clickTime = time + ' ' + timeStr
      timeStr = time + ' ' + timeStr.split('-')[0]
      this.startTime = Date.parse(timeStr)/1000
    }
    // 关闭添加课程弹窗
    handleClose(){
      this.dialogVisible = false;
    }
    // 去除占用弹窗取消
    handleZyClose(){
      this.dialogDeleteStk = false;
    }

    // 去除占用弹窗确定
    handleZyTrue(){
      let data = {
        'course_id': this.deleteCourseId
      }
      this.clearCourse(data)
    }
    // 添加占用弹窗
    alertOccupy(){
      this.dialogAddZy = true;
    }

    async selectCustomer(queryString, cb){
      const res = await this.getCustomer( {name: queryString, phone: queryString, org_id: this.org_id} )
      if(res.status == 200){
        let restaurants = res.data.data.list
        if(restaurants){
          for(var i =0;i < restaurants.length;i++){
            restaurants[i].value = restaurants[i].customer_name
          }
          cb(restaurants)
        }
      }
    }
    // 获取商机数据
    handleSelectBusiness(item){
      this.customerId = item.customer_id
      this.selectBusiness = item.values
    }


    addStkTrue(){
      let data = {
        'campus_id': this.campusId,
        'start_time': this.startTime,
        'course_type': 2,  //1正式 2试听 3占用
        'customer_id': this.customerId,
        'business_id': this.businessId,
        'classroom_id': this.classroomId,
        'sale_employee_id': this.sale_employee_id,
        'remark': this.getStkDesc
      }
      if(this.customerId == '' || this.businessId == '' || this.startTime == '' || this.teacherId == '' || this.sale_employee_id == ''){
        this.$message.error('请将数据填写完整');
        return false
      }

      this.addCurriculum(data)
    }
    // 添加试听课
    handleStkTrue(){
      if(this.isDelete){
        this.addType = 'stk'
        this.deleteClass()
        return false
      }
      this.addStkTrue()
    }
    // 取消添加试听课
    handleStkClose(){
      this.dialogAddStk = false;
    }


    // 获取校区及对应的教室
    async getClassroom(){
      const res = await this.campusClassroom({org_id: this.org_id, campus_id: this.campusId})
      if(res.status == 200){
        if(res.data.data.list && res.data.data.list.length > 0){
          this.classRoom = res.data.data.list[0].values
        }
      }
    }


    // 获取人员数据
    async peopleList(){
      const res = await this.getCampus({types: 'list', org_id: this.org_id})
      if(res.status == 200){
        this.getPeopleList = res.data.data.list
      }
    }

    // 编辑试听课问询弹窗
    alertEditAuditionCourse(){
      this.getClassroom()
      this.peopleList()
      this.editAudition()
    }
    // 编辑正式课问询弹窗
    alertEditAuditionClass(){
      this.editAuditionZsk()
    }
    // 监听商机筛选id
    businessChange(val){
      this.businessId = val
    }
    // 监听上课教师id
    classRoomChange(val){
      this.classroomId = val
    }
    // 监听销售人员筛选id
    peopleListChange(val){
      this.sale_employee_id = val
    }
    // 创建正式课弹窗
    alertFormalCourse(){
      this.dialogAddZsk = true;
      this.getBaseCourse()
      this.getClassroom()
      this.peopleList()
      this.getCourseLevel()
      this.getMaterial()
    }
    // 监听课程种类 && 获取课程名
    changeBaseCourse(val){
      let obj:any = {};
      obj = this.baseCourselist.find((item)=>{
        return item.course_type_id === val
      })
      this.courseTitleList = obj.values
      this.courseTitle = ''
    }
    // 监听课程名
    changeCourseTitle(val){
      this.courseTitleId = val
    }

    // 学员列表查询
    async getStudent(query){
      const res = await this.student({org_id: this.org_id, name: query})
      if(res.status == 200){
        this.studentList = res.data.data.list
      }
    }
    // 获取课程等级
    async getCourseLevel(){
      const res = await this.courseLevel({org_id: this.org_id})
      if(res.status == 200){
        this.courseLevelList = res.data.data.list
      }
    }
    // 监听课程等级
    changeCourseLevel(val){
      this.classLevelId = val
    }
    // 获取素材列表
    async getMaterial(){
      const res = await this.material({org_id: this.org_id ,teacherEmployeeId: this.teacherEmployeeId})
      if(res.status == 200){
        this.materialList = res.data.data.list
        console.log('获取素材列表:',this.materialList)
      }
    }
    // 监听素材
    changeMaterial(val){
      let str:string = val.toString();
      this.materialSelectId = str
    }
    // 监听正式课学员列表
    changeZskStudent(val){
      let arr :any = []
      for(var i=0;i<this.studentList.length;i++){
        for(var j=0;j<val.length;j++){
          if(this.studentList[i].name == val[j]){
            arr.push(this.studentList[i].id)
          }
        }
      }
      this.studentIds = arr
    }
    // 正式课弹窗关闭
    handleZshClose(){
      this.dialogAddZsk = false;
    }
    // 正式课提交方法
    addZskTrue(){
      let week_day: string = this.zskWeekDay.toString()
      // 设置上课日期
      let time:any = this.setZskDate
      let start_date:string = ''
      let end_date: string = ''
      if(time && time.length > 0){
        start_date = Date.parse(time[0])/1000
        end_date = Date.parse(time[1])/1000
      }

      // 是否仅学员可见
      let is_limit_student:number = 1
      if(this.isStudent){
        is_limit_student = 1
      }else{
        is_limit_student = 2
      }

      let data = {
        'campus_id': this.campusId,
        'start_time': this.startTime,
        'course_type': 1,  //1正式 2试听 3占用
        'is_limit_student': is_limit_student,
        'base_course_id': this.courseTitleId,
        'classroom_id': this.classroomId,
        'student_ids': this.studentIds,
        'start_hour': Number(this.startHour),
        'course_level_id': this.classLevelId,
        'material_id': this.materialSelectId,
        'remark': this.zskRemark,
        'subscript': this.zskSubscript,
        'start_date': Number(start_date),
        'end_date': Number(end_date),
        'week_day': week_day
      }
      if(this.courseTitleId == ''|| this.campusId == '' || this.classLevelId == '' || this.materialSelectId == ''){
        this.$message.error('请将数据填写完整');
        return false
      }

      this.addCurriculum(data)
    }
    // 正式课弹窗确认
    handleZshTrue(){
      if(this.isDelete){
        this.addType = 'zsk'
        this.deleteClass()
        return false
      }
      this.addZskTrue()
    }
    // 试听课操作
    handleStk(val){
      this.deleteCourseId = val.id
      this.getCourseSign()
      this.dialogShowStk = true
    }
    // 正式课操作
    handleZsk(val){
      this.deleteCourseId = val.id
      this.getCourseSign()
      this.dialogShowZsk = true;
    }
    // 正式课移除
    handleShowZskTrue(){
      this.dialogDeleteZsk = true
    }
    // 正式课移除弹窗close
    deleteZskClose(){
      this.dialogDeleteZsk = false
    }


    // 正式课移除准备 data
    deleteZskData(){
      let week_day: string = this.deleteWeekDay.toString()
      // 设置上课日期
      let time:any = this.deleteZskDate
      let start_date:string = ''
      let end_date: string = ''
      if(time.length > 0){
        start_date = Date.parse(time[0])/1000
        end_date = Date.parse(time[1])/1000
      }
      let data:any = {}
      if(this.deleteCourseControl == '1'){
        data = {
          'course_id': this.deleteCourseId
        }
      }else{
        data = {
          'campus_id': this.campusId,
          'teacher_employee_id': this.teacherId,
          'start_time': this.startTime,
          'start_date': Number(start_date),
          'end_date': Number(end_date),
          'week_day': week_day,
          'start_hour': Number(this.startHour)
        }
      }
      this.clearCourse(data)
    }


    // 正式课移除弹窗true
    deleteZskTrue(){
      if(this.studentSignList.length > 0){
        this.deleteZskStudent = true
      }else{
        // 直接delete
        this.deleteZskData()
      }
    }

    // 正式课删除问询带学生名称
    handleZskClose(){
      this.deleteZskStudent = false
    }
    handleZskTrue(){
      this.deleteZskData()
      this.handleZskClose()
    }

    //  试听课展示弹窗关闭
    handleShowStkClose(){
      this.dialogShowStk = false
      this.dialogShowZsk = false
    }
    handleShowStkTrue(){
      //问询试听课是否删除
      this.dialogDeleteStk = true
    }
    // 获取课程报名人员
    async getCourseSign(){
      const res = await this.courseSign({org_id: this.org_id, 'course_id': this.deleteCourseId})
      if(res.status == 200){
        this.studentSignList = res.data.data.list
        console.log('报名学生：',res)
      }
    }
    // 编辑优先单个移除
    async deleteClass(){
      let data:any = {
        'course_id': this.deleteCourseId
      }
      const res = await this.deleteCourse( data )
      if(res.status == 200){
        if(this.addType == 'zsk'){
          this.addZskTrue()
        }else{
          this.addStkTrue()
        }
      }
    }
    // 试听课编辑
    async editAudition(){
      this.isDelete = true
      const res = await this.getEditAudition({org_id: this.org_id, 'course_id': this.deleteCourseId,'types': 'edit_info'})
      if(res.status == 200){
        this.getStkDesc = res.data.data.remark
        this.classRoomFirst =res.data.data.classroom_name
        this.classroomId = res.data.data.classroom_id
        this.getPeople = res.data.data.sale_employee_name
        this.sale_employee_id = res.data.data.sale_employee_id
        this.customer = res.data.data.customer_name
        this.customerId = res.data.data.customer_id
        this.business = res.data.data.business_name
        this.businessId = res.data.data.business_id
        this.dialogAddStk = true
      }
    }
    // 正式课编辑
    async editAuditionZsk(){
      this.alertFormalCourse()
      this.isDelete = true
      const res = await this.getEditAudition({'course_id': this.deleteCourseId,'types': 'edit_info'})
      if(res.status == 200){
        this.edit = false
        if(res.data.data.is_limit_student == '1'){
          this.isStudent = true
        }else if(res.data.data.is_limit_student == '2'){
          this.isStudent = false
        }
        if(res.data.data.subscript){
          this.createLabel = '2'
        }
        this.selectBaseCourse = res.data.data.course_type_name
        this.courseTitle = res.data.data.course_name
        this.courseTitleId = res.data.data.base_course_id
        this.classRoomFirst = res.data.data.classroom_name
        this.classroomId = res.data.data.classroom_id
        for(var i=0;i<this.studentSignList.length;i++){
          this.zskStudent.push(this.studentSignList[i].student_name)
        }

        this.zskRemark = res.data.data.remark
        this.classLevelId = res.data.data.course_level_id
        this.classLevel = res.data.data.course_level_name
        this.materialSelectId = res.data.data.material_id
        this.zskSubscript = res.data.data.subscript
        this.dialogAddZsk = true
        this.materialSelect = res.data.data.material_ids
      }
    }
    // 试听课无意向到店
    stkShop(val){
      this.signType = 5
      this.courseType = 2
      this.studentRowData = val
      this.dialogStkShop = true
    }
    // 试听课爽约
    stkSy(val){
      this.signType = 6
      this.courseType = 2
      this.studentRowData = val
      this.dialogStkShop = true
    }
    // 正式课取消预约
    zskCancel(val){
      this.signType = 2
      this.courseType = 1
      this.studentRowData = val
      this.dialogStkShop = true
    }
    // 正式课学生旷课
    zskTruancy(val){
      this.signType = 3
      this.courseType = 1
      this.studentRowData = val
      this.dialogStkShop = true
    }
    // 试听课无意向到店原因提交
    handleStkShopTrue(){
      if(!this.stkReason.desc){
        return false
      }
      let data:any = {
        teacher_remark: this.stkReason.desc,
        sign_type: this.signType,
        id: this.studentRowData.id,
        course_type: this.courseType
      }
      this.signIn(data)
    }
    // 签到方法
    async signIn(data){
      data.org_id = this.org_id
      const res = await this.getClassSign(data)
      if(res.status == 200){
        this.handleStkShopClose()
        this.handleStkSignClose()
        this.handleZskSignClose()
        this.stkShopReason = ''
      }
      console.log('签到成功:',res)
    }
    // 试听课关闭弹窗方法
    handleStkShopClose(){
      this.stkReason.desc = ''
      this.dialogStkShop = false
      this.dialogShowStk = false
    }
    // 试听课签到
    stkSignIn(val){
      this.studentRowData = val
      this.dialogStkSign = true
    }
    // 试听课签到弹窗确认
    handleStkSignTrue(){
      let data = {
        business_status: this.customerIntention,
        course_type: 2,
        id: this.studentRowData.id,
        teacher_remark: this.stkShopReason,
        sign_type: 4
      }
      this.signIn(data)
    }
    // 试听课取消弹窗
    handleStkSignClose(){
      this.dialogStkSign = false
    }
    // 正式课签到
    zskSignIn(val){
      if(val.is_teach_plan == 1){
        // 体系课签到
        this.dialogZskSign = true
      }else{
        // 非体系课签到
        this.dialogZskNoSystem = true
      }
      this.studentRowData = val
      this.getSignList()
      this.getMaterial()
      this.getStudentLevel()

    }
    // 正式课签到取消
    handleZskSignClose(){
      this.dialogZskSign = false
      this.dialogZskNoSystem = false

      this.materialSelect = []
      this.studentRemark = ''
      this.teacherRemark = ''
      this.selectStudentLevel = ''
    }
    // 正式课签到确定
    handleZskSignTrue(){
      let data = {
        "subject_essential_info": this.signPostData,
        "id": this.studentRowData.id,
        "sign_type": 1,
        "sign_student_level_id": this.studentLevelId,
        "course_type": 1,
        "material_id": this.materialSelectList,
        "student_remark": this.studentRemark,
        "teacher_remark": this.teacherRemark
      }
      console.log('签到参数：',data)
      this.signIn(data)
    }
    // 历史签到记录
    async getSignList(){
      const res = await this.getCourseSignLists({'org_id': this.org_id, 'course_id': this.deleteCourseId,'student_id': this.studentRowData.student_id,'types': 'history_list'})
      this.historySelectlist = []
      if(res.status == 200){
        this.historyList = res.data.data.list
        this.signPostData = res.data.data.list
        this.historySignInList = res.data.data.student_info
        this.historySignTime = res.data.data.history_sign_time
        for(var i=0;i<this.historyList.length;i++){
          if(this.historyList[i].percentage != '0'){
            this.historySelectlist.push(this.historyList[i])
          }
        }
      }
    }
    // 监测进度百分比
    changeSchedule(list){
      let data = list.values
      var count = 0
      var len = data.length
      for(var i=0;i<data.length;i++){
        if(data[i].status == 1){
          count += 0
        }else if(data[i].status == 2){
          count += 100/len/2
        }else if(data[i].status == 3){
          count += 100/len
        }
      }
      list.percentage = count

      for(var i=0;i<this.signPostData.length;i++){
        if(this.signPostData[i].subject_id == list.subject_id){
          this.signPostData[i] = list
        }
      }
    }
    // 主题筛选 多选
    changeTheme(val){
      this.historySelectlist = []
      if(val.length == 0){
        return false
      }
      for(var i=0;i<val.length;i++){
        for(var j=0;j<this.historyList.length;j++){
          if(val[i] == this.historyList[j].subject_id){
            this.historySelectlist.push(this.historyList[j])
          }
        }
      }
    }
    // 正式课签到主题删除
    deleteContentList(val){
      for(var j=0;j<this.historySelectlist.length;j++){
        if(val == this.historySelectlist[j].subject_id){
          this.historySelectlist.splice(j, 1);
        }
      }
      for(var j=0;j<this.historyListArr.length;j++){
        if(val == this.historyListArr[j]){
          this.historyListArr.splice(j, 1);
        }
      }
    }
    // 正式课签到学员等级
    async getStudentLevel(){
      const res = await this.studentLevel({org_id: this.org_id})
      if(res.status == 200){
        this.getStudentLevelList = res.data.data.list
      }
    }

    changeSelectMaterial(val){
      let str:string = val.toString()
      this.materialSelectList = str
    }
    changeStudentLevel(val){
      this.studentLevelId = val
    }

    async getCustomerList(val){
      let restaurants = []
      const res = await this.getCustomer( {name: '', phone: '', org_id: this.org_id} )
      if(res.status == 200){
        restaurants = res.data.data.list
        restaurants.forEach(item =>{
          if(item.customer_name == val.data.name){
            this.customerId = item.customer_id
            this.selectBusiness = item.values
          }
        })

      }
    }

    // 创建客户成功调用
    handleCustomerSaved(val) {
      this.customer = val.data.name
      this.getCustomerList(val)
    }
    // 创建客户
    createCustomer(){
      this.toggleModifyDialog({ status: true, data: {} })
    }
    //  调起添加占用试听正式课程问询弹窗
    handlePop(val){
      this.teacherSelect = val.values.teacher_name
      this.teacherId = val.values.id
      this.getClassroom()
      this.peopleList()
      let str:string = ''
      this.getStudent(str)
      this.dialogVisible = true;
    }

    //  添加占用课
    addOccupy(val){
      if(val.type == 'true'){
        let data = {
          'campus_id': this.campusId,
          'start_time': this.startTime,
          'course_type': 3,  //1正式2试听3占用
          'remark': val.desc
        }
        this.addCurriculum(data)
      }
      this.dialogAddZy = false
    }
    //  移除已占用
    handleZy(val){
      this.deleteCourseId = val.id
      this.dialogDeleteZy = true
    }
    //  移除占用课
    deleteOccupy(val){
      if(val == 'true'){
        let data = {
          'course_id': this.deleteCourseId
        }
        this.clearCourse(data)
      }
      this.dialogDeleteZy = false
    }
    //  移除正式课试听课占用课
    async clearCourse(data){
      data.org_id = this.org_id
      const res = await this.deleteCourse( data )
      if(res.status == 200){
        this.dialogDeleteStk = false
        this.dialogAddStk = false
        this.dialogShowStk = false
        this.dialogShowZsk = false
        this.dialogDeleteZsk = false
        this.$message({message: '移除成功', type: 'success'})
        this.getList(this.campusId, this.teacherEmployeeId, this.instrumentTypeId, this.eduTime)
      }
    }
    //  添加试听课问询弹窗
    alertAuditionCourse(){
      this.getClassroom()
      this.peopleList()
      this.dialogAddStk = true
    }


    userHistoryObj: any = {}
    org_id:string = ''
    infoRules: any = infoRules
    loading: boolean = false
    teacherId: string = ''  //teacher id
    addStk:any = {}
    campus: any = [];
    campusSelect: string = ''
    employee: any = []
    employeeSelect: any = []
    teacherSelect: string = ''   // 雇员
    instrument: any = []
    instrumentSelect: any = []
    eduTime: any = ''
    dialogVisible:boolean = false;
    campusId: string = ''           // 校区id
    teacherEmployeeId: string = ''  // 雇员id
    instrumentTypeId: string = ''   // 乐器类型id
    tableData: any[] = []       // list数据
    startTime: string = ''  // 创建课程表时间戳
    clickTime: string = ''  // 创建课程表时间
    customer: string = ''    // stk选择客户字段
    selectBusiness: any = [] // stk选择商机数据数组
    business: string = ''    // stk选择商机数据 字符串
    classRoom: any = []      // stk获取校区对应课程
    classRoomFirst: string = ''  // stk第一次校区对应课程名称
    getPeopleList: any = [] // stk获取人员list
    getPeople: string = '' // stk获取人员
    getStkDesc: string = ''  // 获取stk备注
    customerId: string = ''  // stk客户id
    businessId: string = ''  // stk商机id
    classroomId: string = ''  // stk教师id
    sale_employee_id: string = '' // stk销售人员id
    baseCourselist: any = [] // zsk课程种类list
    selectBaseCourse: string = ''  // zsk课程种类
    courseTitleList: any = []   // zsk课程名list
    courseTitle: string = ''  // zsk 课程名
    courseTitleId: string = '' // zsk 课程名id
    courseLevelList: any = [] // zsk 课程等级list
    classLevel: string = ''   // zsk 课程等级
    classLevelId: string = '' // zsk 课程等级id
    materialList: any = []    // zsk 素材列表
    materialSelect: any = [] // zsk 素材
    materialSelectId: string = ''  // zsk 素材id
    createCourse: string = '1'   // zsk 是否批量建课
    createLabel: string = '1'  // zsk是否创建标签
    isStudent: boolean = true  // zsk是否仅学员可见
    zskRemark: string = ''  // zsk 备注
    zskSubscript: string = ''  // zsk 角标
    setZskDate: any = []   // zsk 日期周期
    deleteZskDate: any = [] //删除正式课日期
    zskWeekDay: any = []  // zsk 设置周几上课
    deleteWeekDay: any = [] // 删除正式课周几
    zskStudent: any = []  // zsk 学员查询
    studentList: any = []   // zsk 学员筛选list
    studentIds: any = [] // zsk 学员选择id
    startHour: string = ''  // zsk 开始时间点数
    deleteCourseId: string = '' //移除id
    dialogDeleteStk: boolean = false // 移除试听课弹窗
    dialogDeleteZsk: boolean = false // 移除正式课弹窗
    deleteCourseControl: string = '1' // 是否批量移除
    studentSignList: any = [] // 课程报名列表
    edit: boolean = true
    isDelete: boolean = false  // 是否是编辑然后删除课程
    dialogAddStk:boolean = false
    dialogShowStk:boolean = false
    dialogShowZsk:boolean = false
    dialogAddZsk:boolean = false
    addType : string = 'stk' // 添加类型
    studentRowData:any = {}  // 签到学生数据
    stkShopReason: string = '' // 试听课无意向到店原因
    stkReason: any = {
      desc: ''
    }                         // 正式课试听课取消原因
    signType: number = 0 // 签到类型  1，2，3，4，5，6
    courseType:number = 0  //1正式 2试听 3占用
    customerIntention: number = 1 // 客户意向 1，2，3
    historyListArr:any = [] // 正式课签到数据item
    selectThemeList:any = [] // 正式课签到已选择主题
    selectThemeHistoryList:any = [] // 正式课历史签到已选择主题
    historyList: any = []  // 正式课历史签到数据
    historySelectlist: any = [] // 正式课签到数据已选择
    getSignInTime: string = '' // 签到时间
    getStudentLevelList: any = [] // 正式课签到学员等级
    selectStudentLevel: string = '' // 正式课签到选择学员等级
    teacherRemark: string = ''  // 正式课签到老师备注
    studentRemark: string = ''  // 正式课签到学生备注
    historySignInList: any = {}   // 历史签到记录
    materialSelectList: string = '' // 正式课签到选择素材list
    studentLevelId: string = ''   // 正式课选择学员等级id
    addCustomer: any = {} // 正式课签到
    dialogStkSign: boolean = false
    dialogStkShop: boolean = false
    dialogZskSign: boolean = false
    dialogZskNoSystem: boolean = false // 非体系课签到
    rowArr:any[] = []
    historySignTime: string = '' // 历史签到记录title
    signPostData: any = []  // 正式课签到提交字符串
    deleteZskStudent: boolean = false // 正式课删除问询带学生名称

    // 新建客户
    addZsk:any = {
      name: '',
      region: '',
      date1: '',
      date2: '',
      delivery: false,
      resource: '',
      desc: '',
      data3: []
    }
    dialogAddZy:boolean = false // 添加占用弹窗
    dialogDeleteZy: boolean = false // 去除占用弹窗
    dialogAddStkData: any = {
      flag: false,
      time: '',
      teacher: '',
      campus: ''
    }  // test addstkdata

  }
</script>
<style lang="scss" >
  .main-container{
    padding-bottom: 0;
  }
  .edu{
    .panel{
      background-color: #fff;
      -webkit-box-flex: 1;
      flex: 1;
      display: -webkit-box;
      display: flex;
      -webkit-box-orient: vertical;
      -webkit-box-direction: normal;
      flex-direction: column;
      margin: 15px;
      border: 1px solid #e2e8f0;
      padding: 15px;
      width: 100%;
      overflow: hidden;
    }
    .header {
      height: 50px;
      line-height: 50px;
    }
    .user_select_con {
      display: flex;
      padding-right: 0 !important;
    }
    .user_select_title{
      text-align: right;
      width: 80px;
      font-size: 15px;
      color: #606266;
      line-height: 50px;
      -ms-flex-negative: 0;
      flex-shrink: 0;
    }
    .user_select_item{
      width: 100%;
    }
    .table{
      margin-top: 10px;
    }
    .table td{
      padding: 0;
      height: 100px;
    }
    .table th div{
      text-align: center;
    }
    .table td div.cell{
      width: 100%;
      text-align: center;
      padding: 0;
    }
    .yzy{
      width: 100%;
      height: 100%;
      background: #ccc;
      text-align: center;
      color: #FFFFFF;
      line-height: 100px;
    }
    .stk{
      width: 100%;
      height: 100%;
      background: green;
      text-align: center;
      color: #FFFFFF;
      line-height: 100px;
      position: relative;
    }
    .zsk{
      width: 100%;
      background: blue;
      line-height: 100px;
      position: relative;
      height: 100px;
    }
    .zsk p{
      line-height: 33px;
      color: #FFFFFF;
      text-align: left;
      padding-left: 3px;
      width: 100%;
    }
  }
  .create_customer{
    display: inline-block;
    margin-left: 10px;
    color: blue;
    cursor: pointer;
  }
  .el-select,.alert_add_stk .el-input,.alert_add_stk .el-textarea{
    width: 80%;
  }
  .alert_add_stk .el-input{
    width: 100%;
  }
  .alert_add_stk .ty_input_class{
    width: 80%;
  }
  .handleShowStkClose th,.handleShowStkClose td{
    text-align: center;
    cursor: pointer;
  }
  .handleShowStkClose td{
    cursor: pointer;
  }
  .alert_add_zsk .el-select,.alert_add_zsk .el-autocomplete{
    width: 100%;
  }
  .alert_add_zsk .el-input,.alert_add_zsk .el-textarea,.alert_add_zsk .el-date-editor{
    width: 90%;
  }
  .alert_add_zsk .el-form-item{
    margin-bottom: 10px;
  }
  .alert_add_zsk .week .el-checkbox{
    margin-right: 5px;
  }
  .triangle{
    height: 40px;
    width: 100px;
    position: absolute;
    overflow: hidden;
    right: -33px;
    top: -8px;
    transform:rotate(45deg);
    -ms-transform:rotate(45deg); /* Internet Explorer */
    -moz-transform:rotate(45deg); /* Firefox */
    -webkit-transform:rotate(45deg); /* Safari 和 Chrome */
    -o-transform:rotate(45deg); /* Opera */
    background: #1890FF;
  }
  .triangle .text{
    position: absolute;
    bottom: 5px;
    background: none;
    border: none;
    outline: none;
    text-align: center;
    width: 100%;
    left: 0;
    color: cyan;
  }
  .alert_delete_zsk .el-checkbox{
    margin-right: 5px;
  }
  .signZsk .el-dialog__body{
    padding-top: 0;
  }
  .signZsk .zsk_sign_title{
    line-height: 30px;
    margin-bottom: 10px;
  }
  .signZsk .zsk_sign_content{
    margin-bottom: 10px;
    padding: 0 44px 0 33px;
  }
  .signZsk .el-collapse{
    border: 0;
  }
  .signZsk .zsk_sign_content .el-input__inner{
    border: none;
    background: #FFFFFF;
  }
  .signZsk .second_content{
    line-height: 40px;
  }
  .signZsk .second_content .el-radio{
    margin-right: 5px;
  }
  .signZsk .second_content span.second_content_title{
    margin-right: 10px;
  }
  .alert_add_stk .must-fill .el-form-item__label:before ,.alert_add_zsk .must-fill .el-form-item__label:before{
    content: '*';
    color: #F56C6C;
    margin-right: 4px;
  }
  .field-form{
    .el-input{
      width: 80%;
    }
    .el-select{
      width: 100%;
    }
  }
</style>
