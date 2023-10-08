const apiUrl = 'https://api.example.com/nonprofit-explorer'; // Replace with the actual API URL

// Make a GET request to the Nonprofit Explorer API
fetch(apiUrl)
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the response as JSON
  })
  .then((data) => {
    // Handle the JSON data here
    console.log(data);

    // You can now work with the 'data' object, which contains the JSON response.
    // Perform operations or display the data as needed.
  })
  .catch((error) => {
    console.error('There was a problem with the fetch operation:', error);
  });
