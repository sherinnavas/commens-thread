from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from .permissions import IsAuthor
from .serializers import (CommentSerializer)
from .models import User,Comments,Post
from rest_framework.response import Response

#List all comments for a post
class CommentList(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request,post_id):
        comment_list = Comments.objects.filter(post=post_id,is_deleted=False,parent_comment=None)
        for i in comment_list:
            print(i.subcomments.all())
        if comment_list.exists():
            serializer = self.serializer_class(instance=comment_list, many=True)
            response =  {
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Comments Fetched',
                'data':serializer.data
            }
        else:
            response = {
            'success' : False,
            'status': status.HTTP_404_NOT_FOUND,
            'message' : "No Comments Found!"
            }
        return Response(response)

#create a comment to a post or a reply to a comment
class CommentCreateView(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request,post_id):
        serializer = self.serializer_class(data=request.data,context={'post_id':post_id})
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            serializer.save()
            response = {
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Comment Added!',
                'data':serializer.data
            }
        else:
            response = {
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Comment Not Created!',
                'data':serializer.errors
            }
        return Response(response)

#Update or delete comments/replies
class CommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,IsAuthor)
    queryset = Comments.objects.filter(is_deleted=False)

    def put(self, request, pk, *args, **kwargs):
        comment_instance =  Comments.objects.get(id= pk)
        if not comment_instance:
            response = {
            'success' : False,
            'message' : "Comment doesn't exist"
            }

        serializer = CommentSerializer(instance = comment_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
            'success' : True,
            'data' : serializer.data,
            'status':status.HTTP_200_OK,
            'message':'Comment Updated!'
            }
        return Response(response)

    def delete(self,request,pk):
        comment = Comments.objects.get(id=pk,is_deleted=False)
        if comment:
            comment.soft_delete()
            replies = comment.subcomments.all()
            for reply in replies:
                reply.soft_delete()
            response = {
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Comment & Replies Deleted!',
            }
        else:
            response = {
            'success': False,
            'status': status.HTTP_404_NOT_FOUND,
            'message' : 'Comment not found'
            }
        return Response(response)
