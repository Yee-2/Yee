var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('select month(OrderDate) as month,sum(Sales) from supermarket WHERE YEAR(OrderDate) = 2019 group by month(OrderDate)', (err, data) => {
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


