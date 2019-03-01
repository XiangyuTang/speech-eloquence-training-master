Scripts 文件夹：
存放项目部署脚本代码，当前文件夹内为空，将在后续实现。

Model文件夹：
存放语音评分模型相关的.py文件。
	-.idea文件夹：
	编辑.py文件使用的IDE Pycharm自动生成的文件夹，与该Python项目有关，请勿人为改动。
	
	-_pycache_文件夹：
	编辑.py文件使用的IDE Pycharm自动生成的文件夹，与该Python项目有关，请勿人为改动。
	
	-venv文件夹：
	编辑.py文件使用的IDE Pycharm自动生成的文件夹，与该Python项目有关，请勿人为改动。
	
	-dict文件夹：
	存放自然语言处理的所需相关词典。
		-BosonNLP_sentiment_score.txt：
		记录各中文词汇的感情色彩。感情色彩用一个带正负的浮点数表示。
		
		-cn_dict.txt:
		记录了所有中文汉字。
		
		-degreeDict.txt:
		记录了所有表示程度的词，并用一个浮点数表示其程度之深浅。
			
		-notDict.txt:
		记录了所有中文否定词。
		
		-stop_words.txt:
		记录了所有中文停用词。
		
		-token_freq_pos%40350k_jieba.txt:
		用于Python的Jieba库实现中文分词。
	
	-sample.wav：
	用于测试的一条wav文件。直接运行Python文件便是分析sample.wav。
		
	-accurate.py：
	包含分析语音发音准确度的函数。
	
	-advice.py：
	包含给出评分和改进意见的函数。
	
	-emotion.py：
	包含分析自然语言和语音包含的感情色彩的函数。
	
	-fluency.py：
	包含分析语音演讲流畅度的函数。
	
	-getPara.py：
	包含获取语音相关参数（如取样率、声道数等）的函数。
	
	-main.py：
	包含主函数。
		
	-proProcess.py：
	包含了对数据集进行预处理的函数。
	
	-tone.py：
	包含了获取声音基频、音量、时长等自然属性的函数。
	
	-trans.py：
	包含了将语音转换为文字功能的函数。

Web-front-end 文件夹：
存放项目前端，包括html文件、css文件、JavaScript文件、相关的图片等资源。
	-css文件夹：
	存放前端的css文件。
		-animate.css:
		控制JQuery动画效果的外观。
		
		-bootstrap-convert.css:
		Bootstrap是Twitter推出的一个用于前端开发的开源工具包。
		本文件稍加修改后用来控制convert.html的全局css样式。
		
		-bootstrap-services.css:
		控制services.html的全局css样式。
		
		-styles-convert.css:
		控制convert.html部分元素的样式。
		
		-styles-services.css:
		控制services.html部分元素的样式。
	
	-images文件夹：
	存放前端需要的图片资源。
	
	-js文件夹：
	存放前端JavaScript文件。
		-jquery.min.js:
		实现弹出、淡入淡出等JQuery动画效果的功能。
		
		-recorder.js:
		实现使用原生JavaScript调用系统录音机的功能。
		
		-convert.js:
		实现项目调用外部API将语音转换为文字的功能。
		
		-wow.min.js:
		实现页面滚动的功能。
		
		-lame.min.js:
		开源的文件。用来实现在浏览器中使用录音机录音的功能。
		
		-worker.js:
		在recorder.js中调用。
		用来开启后台进程，实现实时通信。
		
	-.project:
	前端IDE创建项目生成的文件。
	
	-convert.html:
	实现语音转换文字功能的页面。
	
	-services.html:
	实现在线学习功能的页面，包括调用摄像头、上传录音、录音评分、给出指导意见等功能。