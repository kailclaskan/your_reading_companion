function getTop(results){
    const $top_list = $('#top_books');
    for(result in results){
        let title = results[result].title;
        let author = results[result].author;
        let description = results[result].description;
        $top_list.append(`
            <div class="container my-3">
                <div class='row'>
                    ${title} by ${author}
                </div>
                <div class='row'>
                    ${description}
                </div>
            </div>
        `)
    }
}

getTop();