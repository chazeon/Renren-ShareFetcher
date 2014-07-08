var settings = {"mode": "share", "sort": "date_reversed"}

function SortLib() {
	this.cmpDate = function (a, b) {
		return parseInt(a.date.split(/-/).join("")) - parseInt(b.date.split(/-/).join(""));
	}

	this.cmpDateReverse = function (a, b) {
		return - parseInt(a.date.split(/-/).join("")) + parseInt(b.date.split(/-/).join(""));
	}

	this.cmp = function(a, b) {
		if (settings.sort == "date") {
			return this.cmpDate(a, b);
		} else if (settings.sort == "date_reversed") {
			return this.cmpDateReverse(a, b);

		}

	}
}

cmp = function(a, b) {
	var cmpDate = function (a, b) {
		return parseInt(a.date.split(/-/).join("")) - parseInt(b.date.split(/-/).join(""));
	}

	var cmpDateReverse = function (a, b) {
		return - parseInt(a.date.split(/-/).join("")) + parseInt(b.date.split(/-/).join(""));
	}

	if (settings.sort == "date") {
		return cmpDate(a, b);
	} else if (settings.sort == "date_reversed") {
		return cmpDateReverse(a, b);

	}

}

function View() {
	this.load_share = function () {
		settings.mode = "share"
		this.reload_itemlist(view);
	}

	this.load_collection = function () {
		settings.mode = "collection";
		this.reload_itemlist();
	}

	this.load_sort_date = function() {
		settings.sort = "date";
		$("span#sort-mode").html("Date");
		this.reload_itemlist();
	}

	this.load_sort_date_reversed = function() {
		settings.sort = "date_reversed"
		$("span#sort-mode").html("Date Reversed");
		this.reload_itemlist();
	}

	this.reload_itemlist = function() {
		get_excerpt = function(content) {
			get_match_length = function(content) {
				if (content.match(/[ -~]/g) == null) {
					return 0;
				} else {
					return content.match(/[ -~]/g).length
				}
			}
			get_chn_length = function(content) {
				return content.length - get_match_length(content) / 2
			}

			if (get_chn_length(content) < 19) {
				return content;
			} else {
				var i = 18
				while (get_chn_length(content.substring(0, i)) < 17)
					i++;
				return content.substring(0, i) + "...";
			}
		}
		$("div.menu#postlist").html("");
		$.getJSON("index/" + settings.mode + ".json", function(data) {
			posts = data;
			//slib = new SortLib();
			data.sort(cmp);
			$.each(data, function(key, post){
				$("div.menu#postlist").append("<div class='link item postitem' id=" + key + " data-position='right center'  data-content='" + post.title + "'>" + get_excerpt(post.title) + "</div>");
				$("div.item.postitem#" + key).popup({on: "hover", distanceAway: 20, delay: 300, transition: "fade"});
			})
		})
	}


	this.reload_post_list_height = function() {
		var window_height = $(window).height();
		var fixed_nav_height = $("div.menu#vertical-nav").height();
		var sec_selection_height = $("div.menu#section-menu").height()
		$("div.menu#postlist").height(window_height - fixed_nav_height - sec_selection_height - 36);
	}


}

function Loader() {
	this.load = function() {
		view = new View()
		$("div.sidebar").sidebar("toggle");
		$("div.menu#postlist").on("click", "div.item.postitem", function(){
			$("h1#bigtitle").html(posts[parseInt($(this).attr("id"))].title);
			$("div#post-information").html(posts[parseInt($(this).attr("id"))].date + "<span> </span>" + posts[parseInt($(this).attr("id"))].author_name)
			$.getJSON("blog-json/" +  posts[parseInt($(this).attr("id"))].filename, function(data){
				$("div#article").html(data.data.content);
			});
			$("div.item.postitem").removeClass("active");
			$(this).addClass("active");
		});
		$("div#toggle-sidebar").click(function(){
			$("div.sidebar").sidebar("toggle");
			if ($("iconi.icon#toggle-sidebar").attr("class").split(/ +/).indexOf("left") != -1) {
				$("iconi.icon#toggle-sidebar").removeClass("left").addClass("right");
			} else {
				$("iconi.icon#toggle-sidebar").removeClass("right").addClass("left");
			}
		});
		view.reload_post_list_height();
		$(window).resize(view.reload_post_list_height);
		$("#sec-share").click(function(){view.load_share.call(view)});
		$("#sec-share").addClass("active green")
		$("#sec-collection").click(function(){view.load_collection.call(view)});
		$(".section-select").click(function(){
			$(".section-select").removeClass("active green")
			$(this).addClass("active green")
		})
		//$("div.item#sort-menu").click
		//$("#sort-date").click(function(){view.load_sort_date.call(view)});
		//$("#sort-date-rev").click(function(){view.load_sort_date_reversed.call(view)});
		view.load_share.call(view);
		/*$("div.menu.postitem").on({"mouseenter": function(){
			console.log(this);
			$(this).popup("show");
		}, "mouseleave": function(){
			$(this).popup("hide");
		}})*/
		$("a#sort-menu").popup({on: "click"})
		//$(".section-select").width($("div#section-menu").width() * 0.48)
	}
}

loader = new Loader();
loader.load();


