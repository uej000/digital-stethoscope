<%@ page import="com.gachon.Stethoscope.dto.stethoscopeDto" %>
<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.HashSet" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Stethoscope Dashboard</title>
    <style>
        /* styles.css */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f5f5;
        }

        header {
            background: #4CAF50;
            color: white;
            text-align: center;
            padding: 1rem 0;
        }

        h1 {
            margin: 0;
        }

        main {
            padding: 2rem;
        }

        section {
            margin-bottom: 2rem;
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        h2 {
            margin-top: 0;
            color: #333;
        }
        .person-data {
            display: flex;
            flex-direction: column;
        }

        #data-container {
            font-size: 1.2rem;
            text-align: center;
            align-content: center;
            table {
                width: 90%;
                th {
                    color: #4CAF50;
                }
            }
        }

        #data-container span {
            color: #4CAF50;
            font-weight: bold;
        }

        canvas {
            width: 100%;
            max-height: 95px;
        }
        .top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;

            span {
                text-align: center;
                font-weight: bolder;
                border : 1px solid #ccc;
                border-radius: 5px;
                cursor: pointer;
                width : 50px;
                height: 25px;
            }
        }
        audio {
            width: 100% !important;
        }

        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 1rem 0;
            margin-top: 2rem;
        }

        textarea {
            width: 100%;
            height: 6.25em;
            font-size: 17px;
            border: none;
            resize: none;
        }
    </style>

</head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var table = document.querySelector('table');
        if (table) {
            // 테이블에 클릭 이벤트 리스너 추가
            table.addEventListener('click', function (e) {
                var target = e.target;

                // 이전에 선택된 행을 추적하기 위한 변수
                var previouslySelectedRow = table.querySelector('.selected-row');

                if (target.tagName === 'TD') {
                    var row = target.parentElement; // 클릭된 셀의 부모 행(Row)

                    // 이전 선택된 행 초기화
                    if (previouslySelectedRow) {
                        previouslySelectedRow.classList.remove('selected-row');
                    }


                    // 클릭된 행 활성화
                    row.classList.add('selected-row');

                    // 클릭된 셀 정보를 로그로 출력
                    var name = row.cells[0].textContent;
                    var birth = row.cells[1].textContent;
                    var sex = row.cells[2].textContent;
                    var patientNumber = row.cells[3].textContent;

                    console.log('주민번호:', patientNumber);

                    // AJAX 요청
                    $.ajax({
                        url: '/file',
                        method: 'POST',
                        data: {
                            patientNumber: patientNumber,
                        },
                        xhrFields: {
                            responseType: 'blob', // 파일 데이터를 Blob으로 받기
                        },
                        success: function (response) {
                            console.log('파일 요청 성공');

                            // Blob URL 생성
                            var blobUrl = URL.createObjectURL(response);

                            // 오디오 태그 src 업데이트
                            var audioSource = document.querySelector('audio source');
                            var audioPlayer = document.querySelector('audio');

                            audioSource.src = blobUrl; // Blob URL로 설정
                            audioPlayer.load(); // 변경된 소스를 로드
                        },
                        error: function (xhr, status, error) {
                            console.error('오류 발생:', xhr);
                        },
                    });
                }
            });

// CSS 스타일 추가
            var style = document.createElement('style');
            style.textContent = `
                .selected-row {
                    background-color: #f0f8ff; /* 행 전체의 배경색 */
                    border: 1px solid #add8e6; /* 테두리 스타일 */
                }
            `;
            document.head.appendChild(style);

        }
        $(".refresh_btn").on("click", function(e) {
            $.ajax({
                url: '/main',
                method: 'POST',
                success: function(response) {
                    console.log(e);
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error('오류 발생:', xhr);
                }
            });
        });
    });
</script>
<body>
<header>
    <h1>digital stethoscope</h1>
</header>

<main>
    <!-- Live Data Section -->
    <section class="person-data">
        <div class="top">
            <h2>리스트</h2>
            <span class="refresh_btn">조회</span>
        </div>
        <div id="data-container">
            <%
                ArrayList<stethoscopeDto> list = null;

                String html_tag = null;
                try {
                    list = (ArrayList<stethoscopeDto>) request.getAttribute("stethoscopeDtoList");
                    if (list != null && !list.isEmpty()) {
                        html_tag = "<table><tr><th>이름</th><th>생년월일</th><th>부착위치</th><th>주민번호</th></tr>";
                        for (stethoscopeDto dto : list) {
                            html_tag += "<tr>";
                            html_tag += "<td>" + dto.getName() + "</td>";
                            html_tag += "<td>" + dto.getBirth() + "</td>";
                            html_tag += "<td>" + dto.getPatient_sex() + "</td>";
                            html_tag += "<td>" + dto.getPatient_number() + "</td>";
                            html_tag += "</tr>";
                        }
                        html_tag += "</table>";
                    } else {
                        html_tag = "<p>회원 데이터가 없습니다.</p>";
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                }


            %>
            <%=html_tag%>
        </div>
    </section>

    <!-- Graph Section -->
    <section class="audio">
        <h2>녹음 파일</h2>
        <audio controls>
            <source src="" type="audio/mp3">
            해당 브라우저는 오디오 태그를 지원하지 않습니다.
        </audio>
    </section>

    <section class="feedback">
        <h2>피드백</h2>
        <textarea placeholder="내용을 입력해 주세요."></textarea>
    </section>
</main>

<footer>
    <p>&copy; 고급 프로그래밍2 final-term 3조</p>
</footer>
</body>
</html>
