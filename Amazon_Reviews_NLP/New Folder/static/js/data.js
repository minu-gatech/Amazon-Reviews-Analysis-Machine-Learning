//////////////////////////////////////////////
/* DATA TABLE */
//////////////////////////////////////////////



console.log("READING CSV FILE")
// csv file 
csv_file = 'static/data/amazon_data_small_clean.csv'

// Selecting tbody element of html
var tbody = d3.select("tbody");


/*******************************************************/

// Function to add data - to HTML Table
function addRow(item){
    // Creating a new row into table element
    var row = tbody.append("tr");
    // Reading value in the object and then inserting that values into table row.
    Object.values(item).forEach(value => row.append("td").text(value))   
}



/********************************************************/


function buildTable(data) {

    console.log("INSIDE BUILD TABLE");
    
    //  Counting filtered records
    var records_count = data.length;
    console.log(records_count)

    // Displaying records count on html page
    var h5 = d3.select("#record_count");
    h5.text("RECORDS FOUND : " +  records_count)
    h5.style("color",'white')

    filtered_data = data;

    // First, clear out any existing data
    tbody.html("");
  
    // Calling a function for each item of an array 'filteredData'
    filtered_data.forEach(addRow);

}


/*****************************************************************************/


// Keep Track of all filters
var filters = {};


function filterTable() {

     // Grab the data with d3
     d3.csv(csv_file).then(data => 
        {
            // Set the filteredData to the tableData
            console.log("INSIDE FILTER TABLE");

            let filteredData = data;
        
            // Loop through all of the filters and keep any data that matches the filter values
            console.log("3 - FILTER - " + filters + typeof(filters));

            Object.entries(filters).forEach(([key, value]) => {
            console.log("4 - FILTER - " + filters[key] + key);   
            
            // Selecting column name in csv file according to id of selected menu    
            switch(key) {
                case "review_score":
                    column = "reviews_rating_score";
                    break;
                case "review_recommend":
                    column = "reviews_doRecommend";
                    break;    
                case "review_type":
                    column = "review_rating";
                    break;    
                default:
                    pass    
            }   

            console.log("5 - FILTER - " + column);   
            filteredData = filteredData.filter(row => row[column] === value);
            });
        
            // Finally, rebuild the table using the filtered Data
            buildTable(filteredData);
    
        });
}



/***********************************************************************/

  
function updateFilters() {

    console.log("1 - INSIDE UPDATE FILTERS TABLE"); 

    // Save the value, and id of the filter that was changed
    var filterId = d3.select(this).property('id')
    console.log("filterId - "+filterId)
    var elementValue =  this.options[this.selectedIndex].value
    console.log("elementValue - "+ elementValue)

    // If a filter value was entered then add that filterId and value
    // to the filters list. Otherwise, clear that filter from the filters object
    if (elementValue) {

        if (elementValue == "blank" )
        {
            filters[filterId] = '';
        }
        else
        {
            console.log("yyyyyyyyyyyyyyyyyyyyy")
            filters[filterId] = elementValue;
        }
    }
    else {
        console.log("nnnnnnnnnnnnnnnnnnnnn")
        delete filters[filterId];
    }

    console.log("2 - FILTER - " + filterId +", " +filters[filterId] + typeof(filters));
    // Call function to apply all filters and rebuild the table
    filterTable();

}


/****************************************************************/


// Attach an event to listen for changes to each filter
d3.selectAll(".filter").on("change", updateFilters);





/******************************************************************/
// function to display default contents
function init() 
{
 
    // Grab the data with d3
    d3.csv(csv_file).then(data => 
    {
        // console.log(data)
        var tableData = data;
        // Selecting tbody element of html
        var tbody = d3.select("tbody");
        
        // Calling a function 'addRow'for each item of an array 'tableData'
        tableData.forEach(addRow);
        
        // Displaying total records in console
        console.log(tableData.length)
        
    });
    
}

// Initialize the dashboard
init();
