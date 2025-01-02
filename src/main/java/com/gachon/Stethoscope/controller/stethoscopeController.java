package com.gachon.Stethoscope.controller;

import com.gachon.Stethoscope.dto.stethoscopeDto;
import com.gachon.Stethoscope.service.stethoscopeService;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;

@Controller
@RequestMapping("/")
public class stethoscopeController {

    private final stethoscopeService stethoscopeService;

    @Autowired
    public stethoscopeController(stethoscopeService stethoscopeService) {
        this.stethoscopeService = stethoscopeService;
    }

    @GetMapping("/main")
    public String getData(Model model) {
        List<stethoscopeDto> DtoList = stethoscopeService.getDataList();
        model.addAttribute("stethoscopeDtoList", DtoList);
        return "main";
    }

    @PostMapping("/main")
    public void insertData() {
        stethoscopeService.insertAllData();
    }

    @RequestMapping(value = "/file", method = {RequestMethod.POST, RequestMethod.GET})
    public void getFile(@RequestParam(required = false, defaultValue = "") String patientNumber, HttpServletResponse response) {
        System.out.println("Patient Number: " + patientNumber);
        try {
            stethoscopeService.getFileData(patientNumber, response);
        } catch (IOException e) {
            e.printStackTrace();
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            try {
                response.getWriter().write("Failed to process the file.");
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

//    @GetMapping("/main")
//    public String mainPage() {
//
//        return "main";
//    }


}
