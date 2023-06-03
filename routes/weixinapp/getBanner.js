var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('select * from supermarket', (err, data) => {
        if (err) return console.log(err.message);
        if (data.length === 0) return console.log('数据库无数据');
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


