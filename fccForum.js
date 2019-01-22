const rp = require('request-promise');
const fs = require('fs');
const csv = require('fast-csv');

/**
fccForum.js is a script used to scrape user data from the freeCodeCamp forum website and output the data to a csv
file. The ranks and location of the forum's users are the primary interest, although there are other public variables
available for collection. These variables will be considered later.
**/
var ws = fs.createWriteStream('userData.csv');
let userData = [];
userData.push(['Rank', 'Location']); // Column names for the csv file

/**
collectUsernames takes parameter numPages and returns an array of usernames. The value of numPages determines
how many pages requested to extract usernames. Each page has around 50 usernames. We will use these usernames to
collect locations later. The function getUsernames is called to retrieve a page's worth of usernames.
**/
let collectUserNames = async function(numPages){
  let userNameArray = [];

  for(let page = 0; page < numPages; page++){
    var result = await getUserNames(page);
    userNameArray.push(result);
  }

  return userNameArray;
}

/**
getUserNames takes page as a parameter and returns either an array of usernames obtained from one page or an
error message if the program failed to connect to the url.
**/
function getUserNames(page) {
  let userNameArr = [];
  let pageUrl = "";

  pageUrl = page == 0 ? `https://forum.freecodecamp.org/directory_items?period=weekly&order=likes_received&_=1531683781948`
  : `https://forum.freecodecamp.org/directory_items?likes+received&page=`+ page + `&period=weekly`

  const options = {
    url: pageUrl,
    json : true
  }

  let promise = rp(options)
    .then((data) => {
      for(let index = 0; index < data.directory_items.length; index++){
        userNameArr.push(data.directory_items[index].user.username)
      }
      return userNameArr;
    })
    .catch((err) => {
      console.log(err);
    });

  return promise;
}

/**
getUserLocation takes a username to look up a file that contains their user-defined location. If the user did not
enter any location information, then their location is set to unknown.
**/
function getUserLocation(userName){
  const options = {
    url: `https://forum.freecodecamp.org/u/` + userName + `.json?`,
    json: true,
  }

  let promise = rp(options)
    .then((data) => {
      if(data.user.hasOwnProperty("location"))
        return data.user.location;
      return "Unknown";
    })
    .catch((err) => {
      console.log(err);
    })

  return promise;
}

/**
getMoreData uses a username to look up more data on the user and collects various information like how many they have
given or received, how many posts they've read or solved, etc. This data is completely public on each respective user's
profile. The collected data is returned as an array. This function is not currently called in main().
**/
function getMoreData(userName) {
  let options = {
    url: `https://forum.freecodecamp.org/u/` + userName + `/summary.json?`,
    json: true,
  }

  let promise = rp(options)
    .then((data) => {
      return [data.user_summary.likes_received, data.user_summary.likes_given, data.user_summary.posts_read_count,
        data.user_summary.post_count, data.user_summary.days_visited, data.user_summary.solved_count];
    })
    .catch((err) => {
        console.log(err);
     });

   return promise;
}

/**
This wait function was obtained from Stack Overflow. Its purpose is to make the program wait for some amount of time
in milliseconds to ensure that the program does not overload freeCodeCamp's server with too many requests.
**/
function wait(timeInMs) {
   let startTime = new Date().getTime();
   let currentTime = startTime;

   while(currentTime < startTime + timeInMs) {
     currentTime = new Date().getTime();
  }
}

/**
The main function is responsible for calling all relevant functions to collect user data and writing this data to a csv
file for later processing and visualization.
**/
let main = async function() {
  const userNames = await collectUserNames(2); // Collecting 100 usernames

  let rank = 1;
  for(let row = 0; row < userNames.length; row++){
    for(let col = 0; col < userNames[row].length; col++){

      var location = await getUserLocation(userNames[row][col]);
      wait(10000); // 10 seconds

      if(location != "Unknown") // Only interested in user's who have specified their location
        userData.push([rank, location]);

      process.stdout.write(rank.toString() + " " + userData.length + "|");
      rank++;
    }
  }

  console.log("Final Rank collected" + rank--);
  csv.write([...userData], {headers: true}).pipe(ws);
}

main();
