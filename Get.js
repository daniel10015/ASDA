// Using the Fetch API
let state = 'NY'
fetch('https://projects.propublica.org/nonprofits/api/v2/search.json?q=' + state)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Using async/await
async function getNonprofitData() {
  try {
    const response = await fetch('https://projects.propublica.org/nonprofits/api/v2/search.json?q=' + state);
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

getNonprofitData();
