var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('SELECT MONTH(OrderDate) AS month, category, SUM(quantity) AS quantity FROM supermarket WHERE YEAR(OrderDate) = 2019 GROUP BY month, category;', function(err, data){
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


