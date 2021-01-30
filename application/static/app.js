async function search_book(searchterm){
    $row = $('#top_book_row')
    url = 'https://www.googleapis.com/books/v1/volumes?q='
    resp = await axios.get(`${url}${searchterm}`);
    data = resp.data.items;
    username = $("#user").text();
    res = await axios.get(`/users/search/${username}`)
    $user = res.data
    $row.empty()
    for(let point in data){
        book_card = `<div class="card col-2 my-1 mx-auto">
                        <img src="${data[point]['volumeInfo']['imageLinks']['thumbnail']}" 
                            alt="${data[point]['volumeInfo']['title']}" 
                            class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">${data[point]['volumeInfo']['title']}</h5>
                            <a href="/users/${$user}/library/check/${data[point]['volumeInfo']['title']}" class="btn btn-success my-1">Add to Library</a>
                            <a href="/books/check/${data[point]['volumeInfo']['title']}" class="btn btn-primary my-1">View Details</a>
                        </div>
                    </div>`;
        $row.append(book_card);
    }
}
function findBook(e){
    e.preventDefault();
    $search_term = $("#search_bar").val();
    search_book($search_term);
}

$('#search').on("click", findBook);