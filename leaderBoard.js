
const rp = require('request-promise');
const fs = require('fs');
const csv = require('fast-csv');

var ws = fs.createWriteStream('leaderBoardData.csv');

let table = [];
let userInfo = [];
userInfo.push(['Username', 'Likes Received', 'Likes Given', 'Posts Read Count', 'Post Count',
  'Days Visited','Solved Count', 'Location']);

const options = {
  url: `https://forum.freecodecamp.org/directory_items?period=weekly&order=likes_received&_=1531683781948`,
  json : true //parse json
}

rp(options)
  .then((data) => { //store information in data
    let userData = [];
    for(let users of data.directory_items){
      userData.push({name: users.user.username, likes_received: users.likes_received})
    }
    process.stdout.write('loading');
    getMoreData(userData);
  })
  .catch((err) =>{
    console.log(err);
});

function getMoreData(userData) {
  var i = 0;
  function next() {
    if (i < userData.length){
      var options = {
        url: `https://forum.freecodecamp.org/u/` + userData[i].name + `/summary.json?`,
        json: true,
      }
      rp(options)
        .then((data) => {
          process.stdout.write(`.`);
          table.push([userData[i].name, userData[i].likes_received, data.user_summary.likes_given, data.user_summary.posts_read_count,
            data.user_summary.post_count, data.user_summary.days_visited, data.user_summary.solved_count]);
          ++i;
          return next();
        })
    }
    else
      getLocation(userData);
  }
  return next();
};

function getLocation(userData){
  var i = 0;
  function next() {
    if (i < userData.length){
      var options = {
        url: `https://forum.freecodecamp.org/u/` + userData[i].name + `.json?`,
        json: true,
      }
      rp(options)
        .then((data) => {
          data.user.hasOwnProperty("location") ? userInfo.push([...table[i], data.user.location]):
          userInfo.push([...table[i], "Unknown"]);
          ++i;
          return next();
        })
    }
    else
      csv.write([...userInfo], {headers: true}).pipe(ws);
  }
  return next();
};
