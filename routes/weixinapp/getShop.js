var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('SELECT YEAR(OrderDate)AS YEAR,SUM(quantity) FROM supermarket GROUP BY YEAR ORDER BY SUM(quantity) ;', (err, data) => {
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


