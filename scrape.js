const scrape = require('website-scraper').default;

const options = {
  urls: ['https://www.theroyalbanquetpalace.com/'],
  directory: './scraped_redesign_copy',
  recursive: true,
  maxRecursiveDepth: 3,
  filenameGenerator: 'bySiteStructure',
  urlFilter: function(url) {
    return url.indexOf('theroyalbanquetpalace.com') !== -1;
  },
  request: {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
  }
};

console.log('Starting website scrape...');

scrape(options).then((result) => {
    console.log("Entire website downloaded successfully to ./scraped_redesign_copy/");
}).catch((err) => {
    console.error("An error occurred", err);
});
