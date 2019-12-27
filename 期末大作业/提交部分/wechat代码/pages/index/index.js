//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    answer: ''
  },

  onLoad: function () {
    var self = this;
    wx.request({
      url: 'http://47.107.237.160/?q=help',
      header: {},
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function (res) {
        self.setData({
          answer: res.data
        });
      },
      fail: function (res) { },
      complete: function (res) { },
    })
  },

  submit: function (e) {
    var self = this;
    wx.request({
      url: 'http://47.107.237.160/?q=' + encodeURI(e.detail.value.q),
      header: {},
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        self.setData({
          answer: res.data
        }); 
      },
      fail: function(res) {},
      complete: function(res) {},
    })
  }

})
