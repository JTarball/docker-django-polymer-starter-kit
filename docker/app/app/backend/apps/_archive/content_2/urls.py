from django.conf.urls import patterns, url

from .views import LanguageListView, LanguageDetailView, PostCommentListView, CategoryListView, CommentCardListView, CardListView, CardCreateView, CardCheckImageView, CardAddClickView, CardAddBrokenView, CardAddCommentView, CardAddLikeView, CardCommentsView, CardAddCommentView, SubCategoryListView,CardStatView,  PostDetailView, PostNodeListView, PostUpdateView, SaveContent, MarkdownEditorView, PostTitleView, PostCardStatsView, CardDeleteView

from .models import PostNode, Post

urlpatterns = patterns('', 
    url(r'^markdown_editor/$', MarkdownEditorView.as_view()),
    url(r'^summary/(?P<slug>[\w-]+)/$', PostTitleView.as_view(), name = 'summary' ),
    url(r'^stats/(?P<slug>[\w-]+)/$', PostCardStatsView.as_view(), name = 'like' ),

    url(r'^actions/card/stat/(?P<slug>[\w-]+)/$', CardStatView.as_view(), name = 'card_stat' ),



    url(r'^card/list/(?P<slug>[\w-]+)/$', CardListView.as_view(), name = 'card_list' ),
    url(r'^cardcomments/list/(?P<slug>[\w-]+)/$', CommentCardListView.as_view(), name = 'commentcard_list' ),
    url(r'postcomments/list/(?P<slug>[\w-]+)/$', PostCommentListView.as_view(), name = 'comment_list' ),





    
    url(r'^actions/card/create/(?P<slug>[\w-]+)/$', CardCreateView.as_view(), name = 'card_create' ),
    url(r'^actions/card/check/image/', CardCheckImageView.as_view(), name = 'card_creatddde' ),
    url(r'^actions/card/add/like/(?P<slug>[\w-]+)/$', CardAddLikeView.as_view(), name = 'card_add_like' ),
    url(r'^actions/card/add/click/(?P<slug>[\w-]+)/$', CardAddClickView.as_view(), name = 'card_add_click' ),
    url(r'^actions/card/add/comment/(?P<slug>[\w-]+)/$', CardAddCommentView.as_view(), name = 'card_add_comment' ),
    url(r'^actions/card/delete/(?P<slug>[\w-]+)/$', CardDeleteView.as_view(), name = 'card_delete' ),
    url(r'^actions/card/broken/(?P<slug>[\w-]+)/$', CardAddBrokenView.as_view(), name = 'card_broken' ),
    url(r'^actions/card/comments/(?P<slug>[\w-]+)/$', CardCommentsView.as_view(), name = 'card_comments' ),


    #url(r'^(?P<language>[\w-]+)/(?P<category>[\w-]+)/(?P<subcategory>[\w-]+)/', PostListView.as_view(), name='content:subcategory'),
    
    #url(r'^genres/(?P<slug>\w+)$', 'content.views.show_genres'),
    # /home or /home/                                      -- list all languages
    #url(r'^$', PostNodeListView.as_view(), name='content:postnode_list'),    

    # /home/language  or /home/language/                   -- list all categories for a specific language
    #url(r'^(?P<language>\w+)/$', CategoryListView.as_view(), name='content:category_list'),

    # /home/language/category or /home/language/category/  -- list all subcategories for a specific category
    #url(r'^(?P<language>\w+)/(?P<category>\w+)/$', SubCategoryListView.as_view(), name='content:subcategory_list'),

    # /home/language/category/subcategory or /home/language/category/subcategory/
    #url(r'^(?P<language>\w+)/(?P<category>\w+)/(?P<subcategory>\w+)/$', PostListView.as_view(), name='content:subcategory'),
    

)

# # Dynamic Tree of URLS
# for node in PostNode.objects.all():
#     # find tree structure (files / folders type view)
#     node_str = ''
#     if node.get_ancestors().exists():
#         for nod in node.get_ancestors():
#             node_str += "%s/" % nod
#     # If no ancestors just need node 
#     node_str += "%s" % node
#     # If end node - must be a post/page
#     if node.is_leaf_node(): 
#         #Post.objects.filter()
#         for pos in node.post.all():
#             if pos is not None: 
#                 urlpatterns += patterns('', url(r'^%s/%s' % (node_str, node.post.slug), PostDetailView.as_view(slug_arg ='%s' % node.post.slug)),)
#         else:
#             urlpatterns += patterns('', url(r'^%s/' % (node_str), PostListView.as_view()),)


# / <language> / <category> / <subcategory> / ... etc




# Dynamic (Folder) Tree of URLS
for node in PostNode.objects.all():
    # find tree structure (files / folders type view)
    node_str = ''
    if node.get_ancestors().exists():
        for nod in node.get_ancestors():
            node_str += "%s/" % nod.slug
    # If no ancestors just need node 
    node_str += "%s" % node.slug
    # If end node - must be a post/page
    urlpatterns += patterns('', url(r'^dd/%s/$' % (node_str), PostNodeListView.as_view(node_id='%s' % node.id), name='content:post_folder'))

for post in Post.objects.all():
    node_str = ''
    if post.node is not None:
        print post.node.get_ancestors()
        if post.node.get_ancestors().exists():
            for nod in post.node.get_ancestors():
                node_str += "%s/" % nod.slug
        # If no ancestors just need node 
        node_str += "%s" % post.node.slug
        #urlpatterns += patterns('', url(r'^dd/%s/%s_edit$' % (node_str, post.slug), PostUpdateView.as_view(node_id ='%s' % post.slug)),)
        #urlpatterns += patterns('', url(r'^%s/%s_mddsave$' % (node_str, post.slug), SaveContent.as_view(node_id ='%s' % post.slug), name='content:post_save'),)
        urlpatterns += patterns('', url(r'^dd/%s/%s$' % (node_str, post.slug), PostDetailView.as_view(node_id ='%s' % post.slug), name='content:post_detail'),)
        

