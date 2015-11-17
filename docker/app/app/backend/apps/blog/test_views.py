"""
    blog.test_views.py
    ==================

    Test Views for Blog App

"""
import logging
import datetime

from django.core.urlresolvers import reverse

from django_dynamic_fixture import G
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import AccountsUser
from blog.models import Post
from blog.serializers import PostSerializer

logger = logging.getLogger('test_logger')


class TestPostList(APITestCase):

    def setUp(self):
        self.user = G(AccountsUser, is_superuser=False, is_staff=False)
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)
        self.superadmin = G(AccountsUser, is_superuser=True, is_staff=True)
        self.superadmin_not_staff = G(AccountsUser, is_superuser=True, is_staff=False)
        self.client = APIClient()
        self.url = reverse('blog:list')

    def test_create_post_pass_permissions_superadmin(self):
        """ Test creation of post for superadmin. """
        # Create Post, change slug (has to be unique) so can use it for post
        post = G(Post, author=self.user)
        count = Post.objects.count()
        post.slug = 'different-slug'
        serializer = PostSerializer(post)
        # Force Authentication and Post
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.post(self.url, serializer.data, format='json')
        # Basic check: slug is the same, created & object count increased
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, "%s" % response.data)
        self.assertEquals(Post.objects.count(), count + 1)
        self.assertEquals(response.data['slug'], post.slug, response.data)

    def test_create_post_pass_permissions_staff(self):
        """ Test create permissions for staff. """
        # Testing permissions don't care about data so just generate it first
        post = G(Post, author=self.user)
        count = Post.objects.count()
        post.slug = 'different-slug'
        serializer = PostSerializer(post)
        # Force Authentication and Post
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url, serializer.data, format='json')
        # Basic check: slug is the same, created & object count increased
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Post.objects.count(), count + 1)
        self.assertEquals(response.data['slug'], post.slug)

    def test_create_post_pass_permissions_superadmin_not_staff(self):
        """ Test create permissions for a superadmin who is not staff. """
        # Testing permissions don't care about data so just generate it first
        post = G(Post, author=self.user)
        count = Post.objects.count()
        post.slug = 'different-slug'
        serializer = PostSerializer(post)
        # Force Authentication and Post
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.post(self.url, serializer.data, format='json')
        # Basic check: slug is the same, created & object count increased
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Post.objects.count(), count + 1)
        self.assertEquals(response.data['slug'], post.slug)

    def test_create_post_fail_permissions_user(self):
        """ Test create permissions fail for authenticated users - posts can only be created by staff/superadmin. """
        # Testing permissions don't care about data so just generate it first
        post = G(Post, author=self.user)
        count = Post.objects.count()
        serializer = PostSerializer(post)
        # Force Authentication and Post
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, serializer.data, format='json')
        # Basic check: slug is the same, created & object count increased
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Post.objects.count(), count)
        self.assertEquals(Post.objects.get(pk=post.pk).slug, post.slug)

    def test_get_published_posts_anonymous_user(self):
        """ Tests getting a list of published posts only for anonymous users. """
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=False)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 3, "The list of posts retrieved should only include published ")

    def test_get_published_posts_normal_authenticated_user(self):
        """ Tests getting a list of published posts only for authenticated users. """
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=False)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 3, "The list of posts retrieved should only include published ")

    def test_get_all_posts_superadmin(self):
        """ Test getting a list of all posts for superadmins. """
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=False)
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 4, "The method should retrieve all posts (published & not published).")

    def test_get_all_posts_staff(self):
        """ Tests getting a list of all posts for staff users. """
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=False)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 4, "The method should retrieve all posts (published & not published).")


class TestPostListByYear(APITestCase):

    def setUp(self):
        self.user = G(AccountsUser, is_superuser=False, is_staff=False)
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)
        self.superadmin = G(AccountsUser, is_superuser=True, is_staff=True)
        self.superadmin_not_staff = G(AccountsUser, is_superuser=True, is_staff=False)
        self.client = APIClient()
        self.year = "2015"
        self.url = reverse('blog:list_year', kwargs={'year': self.year})

    def test_post_posts_forbidden_normal_user(self):
        """ Test post action is forbidden for an normal user. """
        G(Post, author=self.user, published=True, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        # Force Authentication and Post
        self.client.force_authenticate(user=self.user)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        response = self.client.post(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_posts_forbidden(self):
        """ Test all posts are retrieved for anonymous user. """
        G(Post, author=self.user, published=True, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        response = self.client.put(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_published_posts_by_year(self):
        """ Test published posts are retrieved. """
        G(Post, author=self.user, published=False, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)


class TestPostListByUser(APITestCase):

    def setUp(self):
        self.user = G(AccountsUser, is_superuser=False, is_staff=False)
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)
        self.client = APIClient()
        self.url = reverse('blog:list_user', kwargs={'user': self.user})

    def test_posts_patch_method_not_allowed(self):
        """ Tests list_user is not allowed for patch method. """
        G(Post, author=self.user, published=True, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_posts_post_method_not_allowed(self):
        """ Tests list_user is not allowed for post method. """
        G(Post, author=self.user, published=True, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_posts_put_method_not_allowed(self):
        """ Tests list_user is not allowed for put method. """
        G(Post, author=self.user, published=True, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.put(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_posts_live_by_user_staff(self):
        """ Test all posts for a specific author are returned for staff. """
        G(Post, author=self.user, published=False, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 3)

    def test_get_posts_by_user(self):
        """ Test published posts for a specific author are returned for anonymous users. """
        G(Post, author=self.user, published=False, updated_at=datetime.date(2014, 3, 13))
        G(Post, author=self.user, published=True)
        G(Post, author=self.user, published=True)
        logger.info("%s" % self.url)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)


class TestPostListByTag(APITestCase):

    def setUp(self):
        self.user = G(AccountsUser, is_superuser=False, is_staff=False)
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)
        self.tag = 'tag1'
        self.client = APIClient()
        self.url = reverse('blog:list_tag', kwargs={'tag': self.tag})

    def test_posts_patch_method_not_allowed(self):
        """ Tests list_tag is not allowed for patch method. """
        G(Post, author=self.user, published=True, tags=[self.tag])
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_post_method_not_allowed(self):
        """ Tests list_tag is not allowed for post method. """
        G(Post, author=self.user, published=True, tags=[self.tag])
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_posts_put_method_not_allowed(self):
        """ Tests list_tag is not allowed for put method. """
        G(Post, author=self.user, published=True, tags=[self.tag])
        G(Post, author=self.user, published=True)
        post = G(Post, author=self.user)
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.put(self.url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_posts_live_by_tag_staff(self):
        """ Test all posts for a specific author are returned for staff. """
        G(Post, author=self.user, published=False, tags=[self.tag])
        G(Post, author=self.user, published=True, tags=[self.tag])
        G(Post, author=self.user, published=True, tags=[self.tag])
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 3)

    def test_get_posts_by_tag(self):
        """ Test published posts for a specific author are returned for anonymous users. """
        G(Post, author=self.user, published=False, tags=[self.tag])
        G(Post, author=self.user, published=True, tags=[self.tag])
        G(Post, author=self.user, published=True, tags=[self.tag])
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)


class TestPostDetail(APITestCase):

    def setUp(self):
        self.user = G(AccountsUser, is_superuser=False, is_staff=False)
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)
        self.superadmin = G(AccountsUser, is_superuser=True, is_staff=True)
        self.superadmin_not_staff = G(AccountsUser, is_superuser=True, is_staff=False)
        self.client = APIClient()

    def test_patch_fail_post_user(self):
        """ Tests patch method is forbidden for a normal user. """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        slug = 'patching'
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {'slug': slug}, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_post_staff(self):
        """ Test patch method for staff is successful. """
        post = G(Post, author=self.user, published=True)
        slug = post.slug
        logger.info("%s" % slug)
        url = reverse('blog:detail', kwargs={'slug': slug})
        slug = 'patching'
        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(url, {'slug': slug}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['slug'], slug)

    def test_patch_post_superadmin(self):
        """ Test patch method for superadmin is successful. """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        slug = 'patching'
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.patch(url, {'slug': slug}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['slug'], slug)

    def test_put_post_superadmin(self):
        """ Test put method is successful for superadmin . """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        post.slug = 'putting'
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['slug'], serializer.data['slug'])

    def test_put_post_staff(self):
        """ Test put method is successful for staff. """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        post.slug = 'putting'
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['slug'], serializer.data['slug'])

    def test_put_fail_not_published_post_user(self):
        """ Test put method fails for normal user on non published post. """
        post = G(Post, author=self.user, published=False)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        serializer = PostSerializer(post)
        logger.info("fdsfdsfd")
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_fail_published_post_user(self):
        """ Test put method fails for normal user on published post. """
        post = G(Post, author=self.user, published=True)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_fail_post_user(self):
        """ Test delete method fails for authenticated users. """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_staff(self):
        """ Test delete method is successful for staff. """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        self.client.force_authenticate(user=self.staff)
        response = self.client.delete(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_superadmin(self):
        """ Test delete method is successful for superadmin. """
        post = G(Post, author=self.user)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.delete(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_post_anonymous_user(self):
        """ Test get method is successful for an anonymous user. """
        post = G(Post, author=self.user, published=True)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        serializer = PostSerializer(post)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_get_post_404_for_non_published_anonymous_user(self):
        """
            Test get post only get published posts for an anonymous user.
            create non published posts -> get it -> 404.
        """
        post = G(Post, author=self.user, published=False)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_not_published_staff(self):
        """ Test get method on non published post by staff is successful. """
        post = G(Post, author=self.user, published=False)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_get_post_not_published_superadmin(self):
        """ Test get method on non published post by superadmin is successful. """
        post = G(Post, author=self.user, published=False)
        slug = post.slug
        url = reverse('blog:detail', kwargs={'slug': slug})
        serializer = PostSerializer(post)
        self.client.force_authenticate(user=self.superadmin_not_staff)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)
