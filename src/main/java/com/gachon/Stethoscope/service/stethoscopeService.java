package com.gachon.Stethoscope.service;

import com.gachon.Stethoscope.dto.stethoscopeDto;
import com.gachon.Stethoscope.mapper.stethoscopeMapper;
import jakarta.servlet.ServletContext;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Service
@Configuration
public class stethoscopeService {

    @Autowired
    private ServletContext servletContext;
    private final stethoscopeMapper stethoscopeMapper;

    @Autowired
    public stethoscopeService(stethoscopeMapper stethoscopeMapper) {
        this.stethoscopeMapper = stethoscopeMapper;
    }

    public List<stethoscopeDto> getDataList() {
        List<stethoscopeDto> stethoscopeDtoList;
        stethoscopeDtoList = stethoscopeMapper.getDataList();
        return stethoscopeDtoList;
    }

    private stethoscopeDto parseFileNameToDto(String fileName) {
        try {
            String baseName = fileName.substring(0, fileName.lastIndexOf('.'));
            String[] parts = baseName.split("-");
            if (parts.length != 4) {
                System.err.println("Invalid file name format: " + fileName);
                return null;
            }

            stethoscopeDto dto = new stethoscopeDto();
            dto.setName(parts[0]);          // 이름
            dto.setBirth(parts[1]);    // 생년월일
            dto.setPatient_sex(parts[2]);       // 성별
            dto.setPatient_number(Integer.valueOf(parts[3])); // 환자번호

            return dto;
        } catch (Exception e) {
            System.err.println("Error parsing file name: " + fileName);
            e.printStackTrace();
            return null;
        }
    }

    public void insertAllData() {
        // 실제 파일 경로 가져오기
        String basePath = servletContext.getRealPath(RELATIVE_PATH);
        File directory = new File(basePath);

        // 디렉토리가 유효한지 확인
        if (!directory.exists() || !directory.isDirectory()) {
            System.err.println("Directory not found: " + basePath);
            return;
        }

        // 파일 목록 가져오기
        File[] files = directory.listFiles();
        if (files == null || files.length == 0) {
            System.err.println("No files found in directory: " + basePath);
            return;
        }

        // 파일 목록을 DTO로 변환하여 DB에 삽입
        List<stethoscopeDto> dtoList = new ArrayList<>();
        for (File file : files) {
            if (file.isFile()) {
                // 파일명을 분석하여 DTO 생성
                stethoscopeDto dto = parseFileNameToDto(file.getName());
                if (dto != null) {
                    dtoList.add(dto);
                }
            }
        }
        stethoscopeMapper.truncate();
        // DB에 삽입
        for (stethoscopeDto dto : dtoList) {
            stethoscopeMapper.insertData(dto);
            System.out.println("Inserted DTO: " + dto);
        }
    }

    private static final String RELATIVE_PATH = "/WEB-INF/sounddata/";

    public void getFileData(String patientNumber, HttpServletResponse response) throws IOException {
        // 실제 파일 경로 가져오기
        String basePath = servletContext.getRealPath(RELATIVE_PATH);
        File directory = new File(basePath);

        if (!directory.exists() || !directory.isDirectory()) {
            System.err.println("Directory not found: " + basePath);
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write("File directory not found");
            return;
        }

        // patientNumber를 포함하는 파일 검색
        File[] matchingFiles = directory.listFiles((dir, name) -> name.contains(patientNumber));

        if (matchingFiles == null || matchingFiles.length == 0) {
            System.err.println("File not found for Patient Number: " + patientNumber);
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            response.getWriter().write("File not found");
            return;
        }

        // 첫 번째 매칭된 파일 선택
        File file = matchingFiles[0];
        System.out.println(matchingFiles[0]);
        // UTF-8로 파일 이름 인코딩
        String encodedFileName = URLEncoder.encode(file.getName(), StandardCharsets.UTF_8.toString());
        encodedFileName = encodedFileName.replace("+", "%20"); // 공백 처리

        // 응답 헤더 설정
        response.setContentType("audio/mp3");
        response.setHeader("Content-Disposition", "attachment; filename*=UTF-8''" + encodedFileName);
        response.setContentLengthLong(file.length());

        // 파일 데이터 스트리밍
        try (FileInputStream fis = new FileInputStream(file);
             OutputStream out = response.getOutputStream()) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                out.write(buffer, 0, bytesRead);
            }
            out.flush();
        }
    }
}

//    public ArrayList<CrawlDto> crawling() {
//        Crawling crawler = new Crawling();
//        return crawler.crawl();
//    }

