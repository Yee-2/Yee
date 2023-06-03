var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('SELECT Subcategories,SUM(quantity) FROM supermarket GROUP BY Subcategories ORDER BY SUM(quantity) DESC LIMIT 0,5', function(err, data){
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


