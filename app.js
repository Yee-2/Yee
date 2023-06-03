var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
let cors = require('cors')

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var getBannerRouter = require('./routes/weixinapp/getBanner');
var getshopRouter = require('./routes/weixinapp/getShop')
var getProfit = require('./routes/weixinapp/getProfit')
var getSales = require('./routes/weixinapp/getSales')
var getYueduzexian = require('./routes/weixinapp/getYueduzexian')
var getDitu = require('./routes/weixinapp/getDitu')
var getpaiming = require('./routes/weixinapp/getpaiming')
var getCustomerName = require('./routes/weixinapp/getCustomerName')
var geiHuanyingcp = require('./routes/weixinapp/geiHuanyingcp')
var getfenlei = require('./routes/weixinapp/getfenlei')

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(cors({origin: '*'}))
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/getBanner',getBannerRouter)
app.use('/getShop',getshopRouter)
app.use('/getProfit',getProfit)
app.use('/getSales',getSales)
app.use('/getYueduzexian',getYueduzexian)
app.use('/getDitu',getDitu)
app.use('/getpaiming',getpaiming)
app.use('/getCustomerName',getCustomerName)
app.use('/geiHuanyingcp',geiHuanyingcp)
app.use('/getfenlei',getfenlei)

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
