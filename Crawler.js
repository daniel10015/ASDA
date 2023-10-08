const axios = require('axios');
const cheerio = require('cheerio');

const url = 'https://www.irs.gov'; // replace with the specific IRS page you want to crawl

axios(url)
  .then(response => {
    const html = response.data;
    const $ = cheerio.load(html);
    const links = [];

    $('a', html).each(function() {
      const link = $(this).attr('href');
      links.push(link);
    });

    console.log(links);
  })
  .catch(console.error);
