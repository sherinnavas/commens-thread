from .models import User,Post,Comments
from rest_framework import serializers

#reusable recursive class for using in recursive fields
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

#serializer for comments
class CommentSerializer(serializers.ModelSerializer):
    #recursive field for grouping the subcomments along with their parent
    subcomments = RecursiveField(many=True,required=False)

    class Meta:
        model = Comments
        fields=('author','body','is_subcomment','created','parent_comment','subcomments')
        extra_kwargs = {'author': {'required': True},'body':{'required':True},'subcomments':{'required':False,'allow_null':True}}

    
    #validation for checking parent comment id is present in case the comment is a reply
    def validate(self, data):
        if data['is_subcomment'] == True and not data['parent_comment']:
            raise serializers.ValidationError("Parent comment not recieved for the subcomment")
        return data

    #get the post id and link respective post to the reply
    def create(self,validated_data):
        post_id = self.context['post_id']
        post = Post.objects.get(id=post_id)
        return Comments.objects.create(post=post,**validated_data)
