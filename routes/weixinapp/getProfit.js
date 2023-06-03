var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('SELECT SUM(profit) FROM supermarket', (err, data) => {
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


