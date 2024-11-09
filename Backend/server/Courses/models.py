from django.db import models





class Course(models.Model):
    
    class PriceStatus(models.Choices):
        FREE = 'FREE'
        PAID = 'PAID'
        
    title = models.CharField(max_length=50)
    
    slug = models.SlugField(max_length=80)
    
    description = models.TextField()
    
    image = models.ImageField(upload_to="Courses/Images/")
    
    video = models.FileField(upload_to="Courses/Videos/")
    
    teacher = models.ForeignKey(
        'Users.User',
        on_delete = models.CASCADE,
        related_name = 'courses'
    )
    
    price_status = models.CharField(
        max_length=5,
        choices=PriceStatus.choices,
        default=PriceStatus.FREE
    )
    
    price = models.BigIntegerField(default=0)
    
    
    
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        
    
    def __str__(self):
        return f'{self.title}---{self.teacher.username}'
    
        


class FAQCourse(models.Model):
    
    question = models.CharField(max_length=255)
    
    answer = models.TextField()
    
    course = models.ForeignKey(
        Course,
        on_delete = models.CASCADE,
        related_name = 'FAQ'
    )
    
    class Meta:
        verbose_name = "FAQ Course"
        verbose_name_plural = "FAQs Course"
        


class DescriptionCourse(models.Model):
    
    title = models.CharField(max_length=255)
    
    description = models.TextField()
    
    course = models.ForeignKey(
        Course,
        on_delete = models.CASCADE,
        related_name = 'Description'
    )
    
    class Meta:
        verbose_name = "Description Course"
        verbose_name_plural = "Descriptions Course"