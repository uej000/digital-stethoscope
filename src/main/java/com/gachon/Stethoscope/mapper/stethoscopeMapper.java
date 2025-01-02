package com.gachon.Stethoscope.mapper;

import com.gachon.Stethoscope.dto.stethoscopeDto;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@Mapper
public interface stethoscopeMapper {
    List<stethoscopeDto> getDataList();
    void insertData(stethoscopeDto stethoscopeDto);
    void truncate();
}
