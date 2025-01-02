package com.gachon.Stethoscope.dto;


import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
public class stethoscopeDto {
    private String name;
    private String birth;
    private String patient_sex;
    private Integer patient_number;
}


